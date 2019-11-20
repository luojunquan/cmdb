# encoding: utf-8
import os
import shutil
from collections import namedtuple
import json

from django.core.management import BaseCommand
from django.conf import settings

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C

from asset.models import Host


class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        if result.task_name == 'collect_host':
            self.collect_host(result._result)
    def collect_host(self, result):
        facts = result.get('ansible_facts', {})
        ip = facts.get('ansible_default_ipv4', {}).get('address', '')
        name = facts.get('ansible_nodename', '')
        mac = facts.get('ansible_default_ipv4', {}).get('macaddress', '')
        os = facts.get('ansible_os_family', '')
        arch = facts.get('ansible_architecture', '')
        mem = facts.get('ansible_memtotal_mb', '')
        cpu = facts.get('ansible_processor_vcpus', '')
        disk = [{'name': i.get('device'), 'total': int(i.get('size_total')) / 1024 / 1024} for i in
                facts.get('ansible_mounts', [])]
        # disk = {i.get('device') : int(i.get('size_total')) / 1024 / 1024 for i in facts.get('ansible_mounts', [])}
        Host.create_or_replace(ip, name, mac, os, arch, mem, cpu, json.dumps(disk))

class Command(BaseCommand):
    def handle(self, *args, **options):
        AnsibleOptions = namedtuple('AnsibleOptions',
                                    ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user',
                                     'check', 'diff'])
        ansible_options = AnsibleOptions(connection='smart', module_path=[], forks=10, become=None, become_method=None,
                                         become_user=None, check=False, diff=False)
        loader = DataLoader()
        passwords = {}
        results_callback = ResultCallback()
        inventory = InventoryManager(loader=loader, sources=os.path.join(settings.BASE_DIR, 'etc', 'hosts'))
        variable_manager = VariableManager(loader=loader, inventory=inventory)
        play_source = {
            'name': "cmdb",
            'hosts': 'all',
            'gather_facts': 'no',
            'tasks': [
                {
                    'name': 'collect_host',
                    'setup': ''
                }
            ]
        }

        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=ansible_options,
                passwords=passwords,
                stdout_callback=results_callback,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
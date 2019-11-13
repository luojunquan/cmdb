#encoding: utf-8

import json


'''
回调

'''
class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        print(result.task_name)
        print(json.dumps({host.name: result._result}, indent=4))



Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
options = Options(connection='smart', module_path=[], forks=10, become=None, become_method=None, become_user=None, check=False, diff=False)


loader = DataLoader()
passwords = {}

results_callback = ResultCallback()

inventory = InventoryManager(loader=loader, sources='hosts') # 剧本的位置

variable_manager = VariableManager(loader=loader, inventory=inventory)

# ansible all -i etc/hosts -m setup
play_source =  {
        'name' : "test",
        'hosts' : 'all', #在哪些主机上执行
        'gather_facts' : 'no',
        'tasks' : [ #执行的任务列表
            {
              'name' : 'fact', #任务名称
              'setup' : ''     #执行任务模块
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
              options=options,
              passwords=passwords,
              stdout_callback=results_callback,
              )
    result = tqm.run(play)
finally:
    if tqm is not None:
        tqm.cleanup()

    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
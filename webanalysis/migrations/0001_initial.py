# Generated by Django 2.0.5 on 2019-12-01 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_id', models.IntegerField(default=0)),
                ('hostname', models.CharField(max_length=526, null=True)),
                ('log_recording', models.CharField(max_length=128, null=True)),
                ('cache_server', models.CharField(max_length=128, null=True)),
                ('user_ip', models.CharField(max_length=128, null=True)),
                ('user_request_ip', models.CharField(max_length=128, null=True)),
                ('http_methond', models.CharField(max_length=128, null=True)),
                ('http_request_host', models.CharField(max_length=128, null=True)),
                ('http_url', models.CharField(max_length=5090, null=True)),
                ('http_status_code', models.IntegerField(default=0, null=True)),
                ('cache_server_port', models.IntegerField(null=True)),
                ('cache_to_user_flow', models.IntegerField(null=True)),
                ('back_to_source_ip', models.CharField(max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccessLogFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
                ('path', models.CharField(default='', max_length=1024)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]

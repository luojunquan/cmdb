# Generated by Django 2.0.5 on 2019-12-02 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webanalysis', '0002_auto_20191202_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesslog',
            name='log_recording',
            field=models.DateTimeField(null=True),
        ),
    ]

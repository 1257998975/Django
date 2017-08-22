# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-22 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('real_name', models.CharField(max_length=20)),
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('user_password', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=40)),
                ('mobile', models.CharField(blank=True, max_length=11)),
                ('isadmin', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='vms',
            fields=[
                ('vm_name', models.CharField(max_length=50)),
                ('vm_uuid', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('vm_purpose', models.TextField()),
                ('vm_comment', models.TextField()),
                ('vm_os_admin', models.IntegerField()),
                ('vm_os_password', models.CharField(blank=True, max_length=20)),
                ('vm_user_id', models.CharField(max_length=20)),
                ('vm_type', models.IntegerField()),
                ('vm_ports', models.CharField(max_length=20)),
                ('vm_ip', models.CharField(max_length=20)),
                ('vm_os', models.CharField(max_length=20)),
                ('vm_cpu', models.IntegerField()),
                ('vm_memory', models.IntegerField()),
                ('vm_disks', models.IntegerField()),
                ('vm_enabled', models.IntegerField(default=False)),
            ],
        ),
    ]
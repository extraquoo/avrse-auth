# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-08-04 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eveauth', '0063_auto_20180609_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='last_login',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='last_logoff',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]

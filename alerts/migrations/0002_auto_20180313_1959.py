# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-13 19:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='webhook',
            old_name='name',
            new_name='event',
        ),
    ]

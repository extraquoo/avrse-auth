# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-11 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timerboard', '0007_auto_20180309_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='timer',
            name='generated',
            field=models.BooleanField(default=False),
        ),
    ]

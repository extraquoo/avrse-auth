# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-15 23:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eveauth', '0055_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='characters',
            field=models.ManyToManyField(related_name='notifications', to='eveauth.Character'),
        ),
    ]

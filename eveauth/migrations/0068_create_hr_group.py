# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-02 11:25
from __future__ import unicode_literals

from django.db import migrations


def add_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    GroupDetails = apps.get_model("eveauth", "GroupDetails")
    hr, hr_created = Group.objects.get_or_create(name="HR")

    if hr_created:
        details = GroupDetails.objects.create(
            group=hr,
            is_open=False,
            can_apply=True,
            forum=True,
            discord=True
        )


class Migration(migrations.Migration):

    dependencies = [
        ('eveauth', '0067_requirement_enabled'),
    ]

    operations = [
        migrations.RunPython(add_groups),
    ]

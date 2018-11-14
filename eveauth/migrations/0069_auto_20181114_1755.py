# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-14 17:55
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0024_auto_20180530_1819'),
        ('eveauth', '0068_create_hr_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirementskill',
            name='recommended_level',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='requirementskill',
            name='required_level',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterUniqueTogether(
            name='requirementskill',
            unique_together=set([('requirement', 'skill')]),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-21 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20180419_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False),
        ),
    ]

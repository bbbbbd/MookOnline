# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-22 05:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20180422_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='datail',
            field=models.TextField(verbose_name='\u8bfe\u7a0b\u8be6\u60c5'),
        ),
    ]
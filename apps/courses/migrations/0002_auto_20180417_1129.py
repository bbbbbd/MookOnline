# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-17 03:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='degree',
            field=models.CharField(choices=[('cj', '\u521d\u7ea7'), ('zj', '\u9ad8\u7ea7'), ('gj', '\u9ad8\u7ea7')], max_length=4, verbose_name='\u8bfe\u7a0b\u96be\u5ea6'),
        ),
    ]
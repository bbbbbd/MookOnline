# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-18 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='\u8bfe\u7a0b\u6807\u7b7e'),
        ),
    ]

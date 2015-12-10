# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151203_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='code_url',
            field=models.URLField(blank=True, null=True, verbose_name='Code Url'),
        ),
        migrations.AddField(
            model_name='user',
            name='project_url',
            field=models.URLField(blank=True, null=True, verbose_name='Project Url'),
        ),
    ]

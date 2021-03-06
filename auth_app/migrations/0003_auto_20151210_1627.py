# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 16:27
from __future__ import unicode_literals

import auth_app.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_auto_20151210_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesstoken',
            name='token',
            field=models.CharField(default=auth_app.utils.generate_token, max_length=255),
        ),
        migrations.AlterField(
            model_name='app',
            name='access_key',
            field=models.CharField(default=auth_app.utils.generate_token, help_text='Access Key', max_length=255),
        ),
        migrations.AlterField(
            model_name='app',
            name='secret_key',
            field=models.CharField(default=auth_app.utils.generate_token, help_text='Secret Key', max_length=255),
        ),
        migrations.AlterField(
            model_name='grant',
            name='token',
            field=models.CharField(default=auth_app.utils.generate_token, max_length=255),
        ),
    ]

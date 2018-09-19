# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-19 14:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20180919_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='uid',
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='second_name',
            field=models.TextField(blank=True, max_length=100),
        ),
    ]

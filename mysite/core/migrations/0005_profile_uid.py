# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-19 14:18
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20180919_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='uid',
            field=models.IntegerField(default=uuid.uuid4),
        ),
    ]

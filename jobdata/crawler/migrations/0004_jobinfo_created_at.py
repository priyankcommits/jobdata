# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-16 16:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0003_jobinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobinfo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 16, 16, 20, 55, 486864, tzinfo=utc)),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-28 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reports', '0007_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='count',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
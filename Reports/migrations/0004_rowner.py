# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-26 06:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Reports', '0003_auto_20170424_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='ROwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reports.ClassRoom')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reports.Exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

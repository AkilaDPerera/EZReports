# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-28 06:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Reports', '0006_auto_20170426_1905'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mr_mrs', models.CharField(choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs.')], default='Mr.', max_length=3)),
                ('parentName', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('msg', models.TextField()),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reports.Student')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
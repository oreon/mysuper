# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-28 22:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20160124_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Name of User')),
                ('maxcap', models.IntegerField(blank=True, max_length=255, verbose_name='Name of User')),
            ],
        ),
    ]

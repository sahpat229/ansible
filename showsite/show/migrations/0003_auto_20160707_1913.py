# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-07 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0002_textfiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textfiles',
            name='lines',
            field=models.FilePathField(path='/etc/ansible/showsite/show/textfiles'),
        ),
    ]

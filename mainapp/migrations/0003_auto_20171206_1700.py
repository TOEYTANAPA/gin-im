# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-06 10:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20171101_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='menu',
            name='price',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='store',
            name='place',
            field=models.CharField(max_length=1000),
        ),
    ]
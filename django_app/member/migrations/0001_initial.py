# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-16 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_type', models.CharField(choices=[('django', 'Basic Login'), ('facebook', 'Facebook Login')], max_length=20)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(default='', max_length=254)),
                ('img_profile', models.CharField(max_length=300)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

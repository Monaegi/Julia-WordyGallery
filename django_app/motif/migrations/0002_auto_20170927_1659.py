# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 07:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('motif', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='name_user',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_author',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='motif',
            name='motif_author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

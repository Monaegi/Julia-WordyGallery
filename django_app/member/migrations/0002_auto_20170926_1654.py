# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 07:54
from __future__ import unicode_literals

from django.db import migrations, models
import utils.fields.custom_imagefields


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='img_profile',
            field=utils.fields.custom_imagefields.CustomImageField(blank=True, default='member/basic_profile.png', upload_to='member'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='user_type',
            field=models.CharField(choices=[('django', 'Basic Login'), ('facebook', 'Facebook Login')], default='django', max_length=20),
        ),
    ]

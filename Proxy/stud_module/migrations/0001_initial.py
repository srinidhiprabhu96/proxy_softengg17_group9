# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 09:19
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=10)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('isPresent', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stud_module_attendance_stud', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('course_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('date', models.DateField(null=True)),
                ('text', models.CharField(max_length=1000)),
                ('isApproved', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stud_module_query_stud', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

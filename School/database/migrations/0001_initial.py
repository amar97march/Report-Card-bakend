# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2019-03-01 10:52
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(2006), django.core.validators.MaxValueValidator(2018)])),
                ('remarks', models.CharField(blank=True, max_length=300)),
                ('marks_in_maths', models.IntegerField(default=-1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('marks_in_english', models.IntegerField(default=-1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('marks_in_hindi', models.IntegerField(default=-1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('marks_in_science', models.IntegerField(default=-1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('marks_in_social', models.IntegerField(default=-1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('principal', models.CharField(default='Not provided', max_length=300)),
                ('established_date', models.DateTimeField(verbose_name='Establishment Date')),
                ('address', models.CharField(default='Not provided', max_length=500)),
                ('school_id', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('div', models.CharField(choices=[('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'), ('V', 'V'), ('VI', 'VI'), ('VII', 'VII'), ('VIII', 'VIII'), ('IX', 'IX'), ('X', 'X'), ('XI', 'XI'), ('XII', 'XII')], max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('first_name', models.CharField(max_length=100)),
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('last_name', models.CharField(max_length=50)),
                ('dob', models.DateField(max_length=8, null=True)),
                ('father_name', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(default='Not provided', max_length=500)),
                ('standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Standard')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacher_name', models.CharField(max_length=200)),
                ('staff_id', models.IntegerField(primary_key=True, serialize=False)),
                ('domain', models.CharField(default='Not provided', max_length=300)),
                ('appointed_date', models.DateTimeField(verbose_name='appointed date')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=2, null=True)),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.School')),
            ],
        ),
        migrations.AddField(
            model_name='standard',
            name='class_teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Teacher'),
        ),
        migrations.AddField(
            model_name='standard',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.School'),
        ),
        migrations.AddField(
            model_name='reportcard',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Student'),
        ),
    ]

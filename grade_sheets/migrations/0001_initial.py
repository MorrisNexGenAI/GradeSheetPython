# Generated by Django 5.2.1 on 2025-05-21 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GradeSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gradesheet', models.JSONField()),
                ('score', models.FloatField(null=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grade_sheets.level')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grade_sheets.period')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grade_sheets.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grade_sheets.subject')),
            ],
        ),
    ]

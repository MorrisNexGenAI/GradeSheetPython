# Generated by Django 5.2.1 on 2025-05-19 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_alter_student_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='date_of_birth',
            new_name='dob',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='first_name',
            new_name='firstName',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='last_name',
            new_name='lastName',
        ),
    ]

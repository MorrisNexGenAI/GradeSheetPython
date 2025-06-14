# Generated by Django 5.2.1 on 2025-06-12 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pass_and_failed', '0002_passfailedstatus_grades_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passfailedstatus',
            name='status',
            field=models.CharField(choices=[('PASS', 'Pass'), ('FAIL', 'Failed'), ('CONDITIONAL', 'Pass Under Condition'), ('INCOMPLETE', 'Incomplete'), ('PENDING', 'Pending')], default='INCOMPLETE', max_length=12),
        ),
    ]

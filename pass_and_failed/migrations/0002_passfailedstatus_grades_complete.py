# Generated by Django 5.2.2 on 2025-06-11 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pass_and_failed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='passfailedstatus',
            name='grades_complete',
            field=models.BooleanField(default=False),
        ),
    ]

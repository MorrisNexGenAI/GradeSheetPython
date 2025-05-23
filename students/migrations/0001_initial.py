# Generated by Django 5.2.1 on 2025-05-16 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('age', models.PositiveIntegerField()),
                ('favorite_color', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=35)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('skin_tone', models.CharField(choices=[('L', 'Light'), ('D', 'Dark'), ('W', 'White'), ('B', 'Brown')], max_length=1)),
                ('nationality', models.CharField(choices=[('AFR', 'African'), ('AS', 'Asian'), ('A', 'American'), ('EU', 'European')], max_length=3)),
            ],
        ),
    ]

# Generated by Django 4.2.11 on 2024-03-13 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_customuser_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='password',
        ),
    ]

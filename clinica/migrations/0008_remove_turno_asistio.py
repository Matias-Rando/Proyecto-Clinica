# Generated by Django 3.1.3 on 2020-11-28 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0007_auto_20201127_2102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='asistio',
        ),
    ]

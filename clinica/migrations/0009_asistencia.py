# Generated by Django 3.1.3 on 2020-11-28 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0008_remove_turno_asistio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
            ],
        ),
    ]

# Generated by Django 3.1.3 on 2020-11-23 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0002_turno'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
            ],
        ),
    ]

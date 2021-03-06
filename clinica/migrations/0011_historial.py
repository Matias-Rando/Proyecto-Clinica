# Generated by Django 3.1.3 on 2020-11-30 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clinica', '0010_turno_asistencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(max_length=64)),
                ('detalle', models.TextField()),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.paciente')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

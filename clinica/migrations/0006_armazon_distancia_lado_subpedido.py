# Generated by Django 3.1.3 on 2020-11-25 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0005_estado_pedido_tipopago'),
    ]

    operations = [
        migrations.CreateModel(
            name='Armazon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Distancia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Lado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Subpedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('armazon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.armazon')),
                ('distancia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.distancia')),
                ('lado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.lado')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.producto')),
            ],
        ),
    ]

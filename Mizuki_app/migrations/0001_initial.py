# Generated by Django 5.0.3 on 2024-03-10 00:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('completed', models.BooleanField(default=False, verbose_name='Orden completada')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('price', models.PositiveIntegerField(verbose_name='Precio')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Cantidad')),
                ('orderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mizuki_app.order')),
                ('productID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mizuki_app.product')),
            ],
        ),
    ]
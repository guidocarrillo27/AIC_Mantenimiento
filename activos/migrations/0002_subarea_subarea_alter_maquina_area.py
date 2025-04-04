# Generated by Django 5.1.6 on 2025-02-19 18:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subarea',
            name='subarea',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='activos.area'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='maquina',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activos.subarea'),
        ),
    ]

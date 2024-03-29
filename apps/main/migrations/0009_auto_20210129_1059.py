# Generated by Django 3.1.5 on 2021-01-28 21:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210129_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoriamovimientofinanciero',
            name='tipo_movimiento_financiero',
            field=models.IntegerField(choices=[(0, 'Gasto'), (1, 'Ingreso')], default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movimientofinanciero',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2021, 1, 28, 21, 59, 21, 558304, tzinfo=utc)),
        ),
    ]

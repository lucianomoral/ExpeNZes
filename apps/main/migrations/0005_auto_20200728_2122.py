# Generated by Django 3.0.8 on 2020-07-28 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200728_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimientofinanciero',
            name='cuenta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.Cuenta'),
        ),
    ]
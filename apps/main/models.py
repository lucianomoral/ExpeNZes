from django.conf import settings
from django.db import models
from django.db.models.enums import Choices
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CategoriaMovimientoFinanciero (models.Model):

    class TipoCategoriaMovimientoFinanciero(models.IntegerChoices):
        GASTO = 0, _('GASTO')
        INGRESO = 1, _('INGRESO')

    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    tipo_categoria_movimiento_financiero = models.IntegerField(choices = TipoCategoriaMovimientoFinanciero.choices)

    def __str__(self):
        return self.nombre

class MovimientoFinanciero (models.Model):
    id = models.AutoField(primary_key = True)
    monto = models.DecimalField(decimal_places=2, max_digits=20)
    categoria_movimiento_financiero = models.ForeignKey('CategoriaMovimientoFinanciero', on_delete = models.PROTECT)
    cuenta = models.ForeignKey('Cuenta', on_delete = models.PROTECT)
    #cuenta = models.IntegerField()
    comentario = models.CharField(max_length=1000, null=True, blank=True)
    fecha = models.DateField(default=timezone.now())
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)

class Cuenta (models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    saldo = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    moneda = models.CharField(max_length=3)

    def __str__(self):
        return self.nombre
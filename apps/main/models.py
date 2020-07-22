from django.conf import settings
from django.db import models

# Create your models here.

class CategoriaMovimientoFinanciero (models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class MovimientoFinanciero (models.Model):
    id = models.AutoField(primary_key = True)
    monto = models.DecimalField(decimal_places=2, max_digits=20)
    categoria_movimiento_financiero = models.ForeignKey('CategoriaMovimientoFinanciero', on_delete = models.PROTECT)
    comentario = models.CharField(max_length=1000)
    fecha = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)
from django.contrib import admin
from .models import CategoriaMovimientoFinanciero, MovimientoFinanciero, Cuenta

# Register your models here.

admin.site.register(CategoriaMovimientoFinanciero)
admin.site.register(MovimientoFinanciero)
admin.site.register(Cuenta)
from django.contrib import admin
from .models import CategoriaMovimientoFinanciero, MovimientoFinanciero

# Register your models here.

admin.site.register(CategoriaMovimientoFinanciero)
admin.site.register(MovimientoFinanciero)
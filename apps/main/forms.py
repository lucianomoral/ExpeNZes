from django import forms
from .models import MovimientoFinanciero

class MovimientoFinancieroForm(forms.ModelForm):
    class Meta:
        model = MovimientoFinanciero
        #fields = '__all__'
        fields = ('id', 'monto', 'categoria_movimiento_financiero','comentario', 'fecha')
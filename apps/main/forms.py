from django import forms
from django.db.models import fields
from django.db.models.fields.mixins import FieldCacheMixin
from .models import MovimientoFinanciero, Cuenta, CategoriaMovimientoFinanciero

"""
class MovimientoFinancieroForm(forms.ModelForm):
    class Meta:
        model = MovimientoFinanciero
        #fields = '__all__'
        fields = ('id', 'monto', 'categoria_movimiento_financiero','comentario', 'fecha', 'cuenta')
"""
class MovimientoFinancieroForm(forms.Form):

    categoria_movimiento_financiero = forms.ModelChoiceField(queryset=CategoriaMovimientoFinanciero.objects.all())
    #tipo_categoria_movimiento_financiero = forms.ChoiceField(choices=get_tipos_categoria_movimiento_financiero_choices(), required=False)
    tipo_categoria_movimiento_financiero = forms.ChoiceField(choices=[], required=False)
    monto = forms.DecimalField()
    comentario = forms.CharField(max_length=1000, required=False)
    fecha = forms.DateField()
    cuenta = forms.ModelChoiceField(queryset=Cuenta.objects.all())

    #Iniciamos el form y le cargamos los choices al campo Tipo de Categoria Movimiento Financiero
    def __init__(self, *args, **kwargs):
        super(MovimientoFinancieroForm, self).__init__(*args, **kwargs)

        tipos = [(0, '--------')]

        for categoria in CategoriaMovimientoFinanciero.objects.all():
            tipos.append((categoria.id, "GASTO" if categoria.tipo_categoria_movimiento_financiero == 0 else "INGRESO"))

        self.fields['tipo_categoria_movimiento_financiero'].choices = tipos

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ('id', 'nombre', 'moneda')

class CategoriaMovimientoFinancieroForm(forms.ModelForm):
    class Meta:
        model = CategoriaMovimientoFinanciero
        fields = ('id', 'nombre', 'tipo_categoria_movimiento_financiero')
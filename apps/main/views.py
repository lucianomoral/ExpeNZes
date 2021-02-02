#Functions
from typing import List
from django.db import models
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, request

#Views
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
#from django.contrib.auth import views as auth_views

#Models
#from django.contrib.auth.models import User
from .models import CategoriaMovimientoFinanciero, MovimientoFinanciero, Cuenta

#Forms
from .forms import MovimientoFinancieroForm, CuentaForm, CategoriaMovimientoFinancieroForm

#Otros
from decimal import Decimal as D

# Create your views here.

@method_decorator(login_required(login_url='/'), name='dispatch')
class MovimientoFinancieroList(ListView):
    model = MovimientoFinanciero
    template_name = 'listarMovimientosFinancieros.html'

    """def get_queryset(self):

        if self.request.user.is_authenticated:

            movimientos_financieros_de_usuario_logueado = self.model.objects.filter(user = self.request.user)
            
            self.queryset = movimientos_financieros_de_usuario_logueado

            return self.queryset"""

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MovimientoFinancieroList, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        
        context['cuentas'] = Cuenta.objects.filter(user = self.request.user)
        context['movimientos_financieros'] = self.model.objects.filter(user = self.request.user)

        return context

@method_decorator(login_required(login_url='/'), name='dispatch')
class MovimientoFinancieroCreate(CreateView):
    model = MovimientoFinanciero
    form_class = MovimientoFinancieroForm
    template_name = 'crearMovimientoFinanciero.html'
    success_url = reverse_lazy('listarMovimientosFinancieros')

    def post(self, request, *args, **kwargs):

        #Obtenemos todos los datos que vienen en el POST y los asignamos a las variables correspondientes
        categoria = CategoriaMovimientoFinanciero.objects.get(pk=request.POST.get("categoria_movimiento_financiero"))
        #Si el "Tipo de Categoria de Movimiento Financiero" es igual 0 (GASTO) entonces se guarda en negativo, caso contrario en positivo
        monto = -abs(D(request.POST.get("monto"))) if categoria.tipo_categoria_movimiento_financiero == 0 else abs(D(request.POST.get("monto")))
        cuenta = Cuenta.objects.get(pk=request.POST.get("cuenta"))
        fecha = request.POST.get("fecha")
        comentario = request.POST.get("comentario")
        usuario = request.user

        #Creamos el nuevo movimiento
        mf = MovimientoFinanciero(monto= monto, categoria_movimiento_financiero=categoria, cuenta=cuenta, comentario=comentario, fecha=fecha, user=usuario)

        mf.save()

        #Actualizamos el saldo de la cuenta
        cuenta.saldo = cuenta.saldo + monto

        cuenta.save()

        return HttpResponseRedirect('/listarMovimientosFinancieros/')

        """
        form = self.form_class(request.POST)

        if form.is_valid():
            
            form_con_user = form.save(commit=False)

            form_con_user.user = request.user

            form_con_user.save()

            #Acá se implementaría la lógica para cambiar el saldo de la cuenta al crear

            c = Cuenta.objects.get(pk=form_con_user.cuenta.id)

            c.saldo = c.saldo + form_con_user.monto

            c.save()
        """

    def get(self, request, *args, **kwargs):

        form = self.form_class()

        form.fields['categoria_movimiento_financiero'].queryset = CategoriaMovimientoFinanciero.objects.filter(user=request.user)

        form.fields['cuenta'].queryset = Cuenta.objects.filter(user=request.user)

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required(login_url='/'), name='dispatch')
class MovimientoFinancieroUpdate(UpdateView):
    model = MovimientoFinanciero
    form_class = MovimientoFinancieroForm
    template_name = 'actualizarMovimientoFinanciero.html'
    success_url = reverse_lazy('listarMovimientosFinancieros')

    def post(self, request, pk):
        
        #Traigo el movimiento registrado en la base
        mf = MovimientoFinanciero.objects.get(pk=pk)

        #Traigo el monto del movimiento registrado
        monto_anterior = mf.monto

        #Traigo la cuenta del movimiento registrado
        cuenta_anterior = Cuenta.objects.get(pk=mf.cuenta.id)

        #Actualizo con los nuevos valores recibidos
        mf.categoria_movimiento_financiero = CategoriaMovimientoFinanciero.objects.get(pk=request.POST.get('categoria_movimiento_financiero'))
        mf.monto = -abs(D(request.POST.get("monto"))) if mf.categoria_movimiento_financiero.tipo_categoria_movimiento_financiero == 0 else abs(D(request.POST.get("monto")))
        mf.cuenta = Cuenta.objects.get(pk=request.POST.get('cuenta'))
        mf.fecha = request.POST.get('fecha')
        mf.comentario = request.POST.get('comentario')

        #Si la cuenta anterior es distinta de la nueva entonces a la cuenta nueva le sumo el valor del monto nuevo
        if int(cuenta_anterior.id) != int(request.POST.get('cuenta')):

            cuenta_nueva = Cuenta.objects.get(pk=request.POST.get('cuenta'))

            cuenta_nueva.saldo = cuenta_nueva.saldo + mf.monto

            #Ya actualizamos el saldo de la cuenta nueva
            cuenta_nueva.save()

        #En caso de que las cuentas sean iguales entonces le sumo el nuevo monto a la cuenta anterior
        else:

            cuenta_anterior.saldo = cuenta_anterior.saldo + mf.monto

        #No importa cual sea el caso, a la cuenta anterior se le resta el monto original
        cuenta_anterior.saldo = cuenta_anterior.saldo - monto_anterior

        #Guardamos los nuevos datos del movimiento y el saldo de la cuenta anterior
        mf.save()

        cuenta_anterior.save()

        return HttpResponseRedirect('/listarMovimientosFinancieros/')

    def get(self, request, pk):

        mf = MovimientoFinanciero.objects.get(pk=pk)

        initial_data = {'categoria_movimiento_financiero': mf.categoria_movimiento_financiero, 'tipo_categoria_movimiento_financiero': mf.categoria_movimiento_financiero, 'monto': abs(mf.monto), 'cuenta': mf.cuenta, 'fecha':mf.fecha, 'comentario': mf.comentario,}

        if request.user != mf.user:

            return HttpResponseRedirect('/listarMovimientosFinancieros/')

        else:
            
            form = self.form_class(initial=initial_data)

            form.fields['categoria_movimiento_financiero'].queryset = CategoriaMovimientoFinanciero.objects.filter(user=request.user)
            form.fields['cuenta'].queryset = Cuenta.objects.filter(user=request.user)

            return render(request, self.template_name, {'form': form})
            

@method_decorator(login_required(login_url='/'), name='dispatch')
class MovimientoFinancieroDelete(DeleteView):
    model = MovimientoFinanciero
    form_class = MovimientoFinancieroForm
    template_name = 'confirmarEliminarMovimientoFinanciero.html'
    success_url = reverse_lazy('listarMovimientosFinancieros')

    def get(self, request, pk):

        mf = MovimientoFinanciero.objects.get(pk=pk)

        if request.user != mf.user:

            return HttpResponseRedirect('/listarMovimientosFinancieros/')

        else:
            
            return render(request, self.template_name)

    def post(self, request, pk):

        mf = MovimientoFinanciero.objects.get(pk=pk)

        if request.user != mf.user:

            return HttpResponseRedirect('/listarMovimientosFinancieros/')

        else:
        
            c = Cuenta.objects.get(pk = mf.cuenta.id)

            c.saldo = c.saldo - mf.monto

            c.save()

            mf.delete()

            return HttpResponseRedirect('/listarMovimientosFinancieros/')

@method_decorator(login_required(login_url='/'), name='dispatch')
class CuentaList(ListView):
    model = Cuenta
    template_name = 'listarCuentas.html'

    #Modificacion del QuerySet para que solo traiga lo del usuario logueado
    def get_queryset(self):

        return super().get_queryset().filter(user = self.request.user)

@method_decorator(login_required(login_url='/'), name='dispatch')
class CuentaCreate(CreateView):
    model = Cuenta
    template_name = 'crearCuenta.html'
    form_class = CuentaForm
    success_url = reverse_lazy('listarCuentas')

    #Cuando creamos la cuenta lo que hacemos es agregarle el id del usuario que la está creando
    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():
            
            form_con_user = form.save(commit=False)

            form_con_user.user = request.user

            form_con_user.save()

            #Acá se implementaría la lógica para cambiar el saldo de la cuenta al crear

            return HttpResponseRedirect('/listarCuentas/')

@method_decorator(login_required(login_url='/'), name='dispatch')
class CuentaUpdate(UpdateView):
    model = Cuenta
    template_name = 'actualizarCuenta.html'
    form_class = CuentaForm
    success_url = reverse_lazy('listarCuentas')

    #Nos fijamos si la cuenta que se va a actualizar es del mismo usuario logueado.
    def get(self, request, pk):

        c = Cuenta.objects.get(pk=pk)

        if request.user != c.user:

            return HttpResponseRedirect('/listarCuentas/')

        else:
            
            form = self.form_class(instance=c)
            
            return render(request, self.template_name, {'form': form})

@method_decorator(login_required(login_url='/'), name='dispatch')
class CuentaDelete(DeleteView):
    model = Cuenta
    template_name = 'confirmarEliminarCuenta.html'
    form_class = CuentaForm
    success_url = reverse_lazy('listarCuentas')

    #Nos fijamos si la cuenta que se va a eliminar es del mismo usuario logueado.
    def get(self, request, pk):

        c = Cuenta.objects.get(pk=pk)

        if request.user != c.user:

            return HttpResponseRedirect('/listarCuentas/')

        #Si la cuenta tiene movimientos asociados entonces se impide la eliminacion
        elif len(MovimientoFinanciero.objects.filter(cuenta = c)) > 0:
            
            return render(request, self.template_name, {"mensaje": "No se puede eliminar la cuenta porque tiene movimientos asociados. Proceda a eliminar los movimientos y luego elimine la cuenta."})

        #Si es la cuenta del mismo usuario logueado y no tiene movimientos, entonces dejamos eliminar
        else:
            
            return render(request, self.template_name)

@method_decorator(login_required(login_url='/'), name='dispatch')
class CategoriaMovimientoFinancieroList(ListView):
    model = CategoriaMovimientoFinanciero
    template_name = 'listarCategoriasMovimientoFinanciero.html'

    #Devolvemos las categorias que son solo del usuario logueado
    def get_queryset(self):
        return super().get_queryset().filter(user = self.request.user)

@method_decorator(login_required(login_url='/'), name='dispatch')
class CategoriaMovimientoFinancieroCreate(CreateView):
    model = CategoriaMovimientoFinanciero
    template_name = 'crearCategoriaMovimientoFinanciero.html'
    form_class = CategoriaMovimientoFinancieroForm
    success_url = reverse_lazy('listarCategoriasMovimientoFinanciero')

    #Cuando creamos la cuenta lo que hacemos es agregarle el id del usuario que la está creando
    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():
            
            form_con_user = form.save(commit=False)

            form_con_user.user = request.user

            form_con_user.save()

            return HttpResponseRedirect('/listarCategoriasMovimientoFinanciero/')


@method_decorator(login_required(login_url='/'), name='dispatch')
class CategoriaMovimientoFinancieroUpdate(UpdateView):
    model = CategoriaMovimientoFinanciero
    template_name = 'actualizarCategoriaMovimientoFinanciero.html'
    form_class = CategoriaMovimientoFinancieroForm
    success_url = reverse_lazy('listarCategoriasMovimientoFinanciero')

    #Al pedir la actualizacion nos fijamos que la categoria a actualizar sea del mismo usuario que esta logueado
    def get(self, request, pk):

        c = CategoriaMovimientoFinanciero.objects.get(pk=pk)

        if c.user != request.user:

            return HttpResponseRedirect('/listarCategoriasMovimientoFinanciero/')

        else:
            
            form = self.form_class(instance=c)

            return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        
        c = CategoriaMovimientoFinanciero.objects.get(pk=pk)

        #Para dejar actualizar la categoria nos fijamos que NO tenga movimientos y que NO se le esté cambiando el TIPO. Si tiene movimientos y se cambia el nombre no hay problema 
        if len(MovimientoFinanciero.objects.filter(categoria_movimiento_financiero=c)) > 0 and c.tipo_categoria_movimiento_financiero != int(request.POST.get('tipo_categoria_movimiento_financiero')):

            return render(request, 'confirmarEliminarCategoriaMovimientoFinanciero.html', {'mensaje': "No se puede editar la categoría porque tiene movimientos asociados. Proceda a eliminar los movimientos y luego edite la categoría."})

        else:

            form = self.form_class(request.POST)

            if form.is_valid():
            
                c.nombre = request.POST.get('nombre')
                c.tipo_categoria_movimiento_financiero = request.POST.get('tipo_categoria_movimiento_financiero')

                c.save()

                return HttpResponseRedirect('/listarCategoriasMovimientoFinanciero/')

@method_decorator(login_required(login_url='/'), name='dispatch')
class CategoriaMovimientoFinancieroDelete(DeleteView):
    model = CategoriaMovimientoFinanciero
    template_name = 'confirmarEliminarCategoriaMovimientoFinanciero.html'
    form_class = CategoriaMovimientoFinancieroForm
    success_url = reverse_lazy('listarCategoriasMovimientoFinanciero')

    #Para eliminar el usuario logueado tiene que ser el mismo que el de la categoria
    def get(self, request, pk):
        
        c = CategoriaMovimientoFinanciero.objects.get(pk=pk)

        if request.user != c.user:

            return HttpResponseRedirect('/listarCategoriasMovimientoFinanciero/')

        #Si la categoria tiene movimientos asociados entonces se impide la eliminacion
        elif len(MovimientoFinanciero.objects.filter(categoria_movimiento_financiero = c)) > 0:
            return render(request, self.template_name, {"mensaje": "No se puede eliminar la categoria porque tiene movimientos asociados. Proceda a eliminar los movimientos y luego elimine la categoria."})

        #Si es la cuenta del mismo usuario logueado y no tiene movimientos, entonces dejamos eliminar
        else:
            
            return render(request, self.template_name)

class IndexLogin(TemplateView):
    template_name = 'indexLogin.html'

    def get(self, request):
        
        #Cuando se accede a la pagina del login, si el usuario ya está logueado, se lo redirige a la pagina de los movimientos
        if request.user is None:
            return render(request, self.template_name)
        elif request.user.is_authenticated:
            return redirect('listarMovimientosFinancieros')
        else:
            return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('listarMovimientosFinancieros')
        else:
            return redirect('indexLoginError')

class IndexLoginError(TemplateView):
    template_name = 'indexLoginError.html'

def log_user_out(request):
    logout(request)
    return redirect('/')
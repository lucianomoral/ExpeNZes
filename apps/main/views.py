#Functions
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

#Views
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
#from django.contrib.auth import views as auth_views

#Models
#from django.contrib.auth.models import User
from .models import CategoriaMovimientoFinanciero, MovimientoFinanciero, Cuenta

#Forms
from .forms import MovimientoFinancieroForm


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

        form = self.form_class(request.POST)

        if form.is_valid():
            
            form_con_user = form.save(commit=False)

            form_con_user.user = request.user

            form_con_user.save()

            #Acá se implementaría la lógica para cambiar el saldo de la cuenta al crear

            c = Cuenta.objects.get(pk=form_con_user.cuenta.id)

            c.saldo = c.saldo + form_con_user.monto

            c.save()

            return HttpResponseRedirect('/listarMovimientosFinancieros/')

    def get(self, request, *args, **kwargs):

        form = self.form_class()

        form.fields['cuenta'].queryset = Cuenta.objects.filter(user=request.user)

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required(login_url='/'), name='dispatch')
class MovimientoFinancieroUpdate(UpdateView):
    model = MovimientoFinanciero
    form_class = MovimientoFinancieroForm
    template_name = 'actualizarMovimientoFinanciero.html'
    success_url = reverse_lazy('listarMovimientosFinancieros')

    def post(self, request, pk):
        
        mf = MovimientoFinanciero.objects.get(pk=pk)

        monto_anterior = mf.monto

        form = self.form_class(request.POST, instance=mf)

        if form.is_valid():

            #Acá se va a implementar la lógica para editar el saldo de la cuenta

            c = Cuenta.objects.get(pk=form.cleaned_data['cuenta'].id)

            c.saldo = c.saldo - monto_anterior + form.cleaned_data['monto']

            c.save()

            form.save()

        return HttpResponseRedirect('/listarMovimientosFinancieros/')

    def get(self, request, pk):

        mf = MovimientoFinanciero.objects.get(pk=pk)

        if request.user != mf.user:

            return HttpResponseRedirect('/listarMovimientosFinancieros/')

        else:
            
            form = self.form_class(instance=mf)

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

class IndexLogin(TemplateView):
    template_name = 'indexLogin.html'

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
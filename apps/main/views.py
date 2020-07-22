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
from .models import CategoriaMovimientoFinanciero, MovimientoFinanciero

#Forms
from .forms import MovimientoFinancieroForm


# Create your views here.

@method_decorator(login_required(login_url='/'), name='dispatch')
class MovimientoFinancieroList(ListView):
    model = MovimientoFinanciero
    template_name = 'listarMovimientosFinancieros.html'

    def get_queryset(self):

        if self.request.user.is_authenticated:

            movimientos_financieros_de_usuario_logueado = self.model.objects.filter(user = self.request.user)
            
            self.queryset = movimientos_financieros_de_usuario_logueado

            return self.queryset

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

            return HttpResponseRedirect('/listarMovimientosFinancieros/')

@method_decorator(login_required(login_url='/'), name='dispatch')
class MovimientoFinancieroUpdate(UpdateView):
    model = MovimientoFinanciero
    form_class = MovimientoFinancieroForm
    template_name = 'actualizarMovimientoFinanciero.html'
    success_url = reverse_lazy('listarMovimientosFinancieros')

    def post(self, request, pk):
        
        mf = MovimientoFinanciero.objects.get(pk=pk)

        form = self.form_class(request.POST, instance=mf)

        if form.is_valid():

            form.save()

        return HttpResponseRedirect('/listarMovimientosFinancieros/')

@method_decorator(login_required(login_url='/'), name='dispatch')
class MovimientoFinancieroDelete(DeleteView):
    model = MovimientoFinanciero
    form_class = MovimientoFinancieroForm
    template_name = 'confirmarEliminarMovimientoFinanciero.html'
    success_url = reverse_lazy('listarMovimientosFinancieros')

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
"""ExpeNZes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.main.views import CuentaList, MovimientoFinancieroList, MovimientoFinancieroCreate, MovimientoFinancieroUpdate, MovimientoFinancieroDelete, IndexLogin, log_user_out, IndexLoginError, CuentaList, CuentaCreate, CuentaUpdate, CuentaDelete, CategoriaMovimientoFinancieroList, CategoriaMovimientoFinancieroCreate, CategoriaMovimientoFinancieroUpdate, CategoriaMovimientoFinancieroDelete #, validateLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexLogin.as_view(), name="indexLogin"),
    path('validateLogin/', IndexLogin.as_view(), name="validateLogin"),
    path('indexLoginError/',IndexLoginError.as_view(), name='indexLoginError'),
    path('logout/', log_user_out, name="logout"),
    path('listarMovimientosFinancieros/', MovimientoFinancieroList.as_view(), name='listarMovimientosFinancieros'),
    path('crearMovimientoFinanciero/', MovimientoFinancieroCreate.as_view(), name='crearMovimientoFinanciero'),
    path('actualizarMovimientoFinanciero/<int:pk>', MovimientoFinancieroUpdate.as_view(), name='actualizarMovimientoFinanciero'),
    path('eliminarMovimientoFinanciero/<int:pk>', MovimientoFinancieroDelete.as_view(), name='eliminarMovimientoFinanciero'),
    path('listarCuentas/', CuentaList.as_view(), name='listarCuentas'),
    path('crearCuenta/', CuentaCreate.as_view(), name='crearCuenta'),
    path('actualizarCuenta/<int:pk>', CuentaUpdate.as_view(), name='actualizarCuenta'),
    path('eliminarCuenta/<int:pk>', CuentaDelete.as_view(), name='eliminarCuenta'),
    path('listarCategoriasMovimientoFinanciero/', CategoriaMovimientoFinancieroList.as_view(), name='listarCategoriasMovimientoFinanciero'),
    path('crearCategoriaMovimientoFinanciero/', CategoriaMovimientoFinancieroCreate.as_view(), name='crearCategoriaMovimientoFinanciero'),
    path('actualizarCategoriaMovimientoFinanciero/<int:pk>', CategoriaMovimientoFinancieroUpdate.as_view(), name='actualizarCategoriaMovimientoFinanciero'),
    path('eliminarCategoriaMovimientoFinanciero/<int:pk>', CategoriaMovimientoFinancieroDelete.as_view(), name='eliminarCategoriaMovimientoFinanciero'),
]

from django.urls import path

from .views import consultar_poliza, listar_coberturas, registrar_consumo

urlpatterns = [
    path("polizas/<str:numero>/", consultar_poliza),
    path("polizas/<str:numero>/coberturas/", listar_coberturas),
    path("polizas/<str:numero>/consumos/", registrar_consumo),
]
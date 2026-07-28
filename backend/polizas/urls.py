from django.urls import path

from .views import consultar_poliza

urlpatterns = [
    path("polizas/<str:numero>/", consultar_poliza),
]
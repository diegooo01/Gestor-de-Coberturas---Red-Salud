from django.contrib import admin

from .models import Asegurado, Plan, Cobertura, Poliza, Consumo, PlanCobertura

admin.site.register(Cobertura)
admin.site.register(Plan)
admin.site.register(Poliza)
admin.site.register(Consumo)
admin.site.register(PlanCobertura)
admin.site.register(Asegurado)
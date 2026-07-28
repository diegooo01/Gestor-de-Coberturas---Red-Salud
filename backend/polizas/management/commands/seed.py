from datetime import date, timedelta

from django.core.management.base import BaseCommand

from polizas.models import Asegurado, Plan, Cobertura, Poliza, PlanCobertura, Consumo

class Command(BaseCommand):
    help = "Carga datos de prueba en la base de datos"

    def handle(self, *args, **options):
        self.stdout.write("Inicializando datos...")

        #Se limpia primero los datos
        Consumo.objects.all().delete()
        PlanCobertura.objects.all().delete()
        Poliza.objects.all().delete()
        Cobertura.objects.all().delete()
        Plan.objects.all().delete()
        Asegurado.objects.all().delete()

        #Se crea un asegurado
        asegurado = Asegurado.objects.create(
            numero_documento="12345678",
            nombres="Juan",
            apellidos="Pérez",
        )

        #Se crea un plan
        plan = Plan.objects.create(
            nombre="Plan Salud Total",
            descripcion="Cobertura integral de salud",
        )

        #Se crean coberturas
        consulta = Cobertura.objects.create(nombre="Consulta médica")
        laboratorio = Cobertura.objects.create(nombre="Examen de laboratorio")

        #Se asignan limites segun cobertura
        PlanCobertura.objects.create(plan=plan, cobertura=consulta, limite_usos=10)
        PlanCobertura.objects.create(plan=plan, cobertura=laboratorio, limite_usos=5)

        #Se crea una poliza activa
        hoy = date.today()
        poliza = Poliza.objects.create(
            numero="POL-2025-0001",
            asegurado=asegurado,
            plan=plan,
            fecha_inicio=hoy - timedelta(days=30),
            fecha_fin=hoy + timedelta(days=335),
            estado=Poliza.Estado.ACTIVA,
        )

        #Se registran consumos de las coberturas
        Consumo.objects.create(poliza=poliza, cobertura=consulta)
        Consumo.objects.create(poliza=poliza, cobertura=consulta)

        self.stdout.write(self.style.SUCCESS("Datos de prueba creados correctamente."))
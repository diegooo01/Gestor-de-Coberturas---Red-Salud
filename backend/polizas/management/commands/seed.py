from datetime import date, timedelta
from django.contrib.auth.models import User
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

        #Usuario de prueba para el login
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin", password="admin123")
            self.stdout.write("Usuario de prueba creado: admin / admin123")

        hoy = date.today()

        #Se crean los asegurados
        juan = Asegurado.objects.create(numero_documento="12345678", nombres="Juan", apellidos="Pérez")
        maria = Asegurado.objects.create(numero_documento="87654321", nombres="María", apellidos="García")
        carlos = Asegurado.objects.create(numero_documento="45678912", nombres="Carlos", apellidos="Rojas")
        ana = Asegurado.objects.create(numero_documento="98765432", nombres="Ana", apellidos="Torres")

        #Se crean los planes
        plan_total = Plan.objects.create(nombre="Plan Salud Total", descripcion="Cobertura integral de salud")
        plan_basico = Plan.objects.create(nombre="Plan Básico", descripcion="Cobertura esencial")
        plan_premium = Plan.objects.create(nombre="Plan Premium", descripcion="Cobertura ampliada con especialidades")

        #Se crean coberturas
        consulta = Cobertura.objects.create(nombre="Consulta médica")
        laboratorio = Cobertura.objects.create(nombre="Examen de laboratorio")
        emergencia = Cobertura.objects.create(nombre="Atención de emergencia")
        odontologia = Cobertura.objects.create(nombre="Odontología")
        farmacia = Cobertura.objects.create(nombre="Farmacia")

        #Se asignan limites segun cobertura (la misma cobertura tiene distinto limite en cada plan)
        PlanCobertura.objects.create(plan=plan_total, cobertura=consulta, limite_usos=10)
        PlanCobertura.objects.create(plan=plan_total, cobertura=laboratorio, limite_usos=5)
        PlanCobertura.objects.create(plan=plan_total, cobertura=emergencia, limite_usos=3)

        PlanCobertura.objects.create(plan=plan_basico, cobertura=consulta, limite_usos=4)
        PlanCobertura.objects.create(plan=plan_basico, cobertura=farmacia, limite_usos=6)

        PlanCobertura.objects.create(plan=plan_premium, cobertura=consulta, limite_usos=20)
        PlanCobertura.objects.create(plan=plan_premium, cobertura=laboratorio, limite_usos=15)
        PlanCobertura.objects.create(plan=plan_premium, cobertura=odontologia, limite_usos=8)
        PlanCobertura.objects.create(plan=plan_premium, cobertura=emergencia, limite_usos=5)

        #Se crea una poliza activa y vigente
        poliza = Poliza.objects.create(
            numero="POL-2025-0001",
            asegurado=juan,
            plan=plan_total,
            fecha_inicio=hoy - timedelta(days=30),
            fecha_fin=hoy + timedelta(days=335),
            estado=Poliza.Estado.ACTIVA,
        )

        #Se crea una poliza premium vigente
        poliza2 = Poliza.objects.create(
            numero="POL-2025-0002",
            asegurado=maria,
            plan=plan_premium,
            fecha_inicio=hoy - timedelta(days=60),
            fecha_fin=hoy + timedelta(days=300),
            estado=Poliza.Estado.ACTIVA,
        )

        #Se crea una poliza basica vigente
        Poliza.objects.create(
            numero="POL-2025-0003",
            asegurado=carlos,
            plan=plan_basico,
            fecha_inicio=hoy - timedelta(days=10),
            fecha_fin=hoy + timedelta(days=355),
            estado=Poliza.Estado.ACTIVA,
        )

        #Se crea una poliza vencida (para probar la regla de vigencia)
        Poliza.objects.create(
            numero="POL-2024-0009",
            asegurado=ana,
            plan=plan_total,
            fecha_inicio=hoy - timedelta(days=400),
            fecha_fin=hoy - timedelta(days=35),
            estado=Poliza.Estado.ACTIVA,
        )

        #Se crea una poliza suspendida (para probar la regla de estado)
        Poliza.objects.create(
            numero="POL-2025-0004",
            asegurado=juan,
            plan=plan_premium,
            fecha_inicio=hoy - timedelta(days=20),
            fecha_fin=hoy + timedelta(days=340),
            estado=Poliza.Estado.SUSPENDIDA,
        )

        #Se registran consumos de las coberturas
        Consumo.objects.create(poliza=poliza, cobertura=consulta)
        Consumo.objects.create(poliza=poliza, cobertura=consulta)
        Consumo.objects.create(poliza=poliza, cobertura=consulta)
        Consumo.objects.create(poliza=poliza, cobertura=consulta)
        Consumo.objects.create(poliza=poliza, cobertura=laboratorio)
        Consumo.objects.create(poliza=poliza2, cobertura=consulta)
        Consumo.objects.create(poliza=poliza2, cobertura=odontologia)

        self.stdout.write(self.style.SUCCESS("Datos de prueba creados correctamente."))
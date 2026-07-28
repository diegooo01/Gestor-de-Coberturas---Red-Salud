from django.db import models

class Asegurado(models.Model):
    numero_documento = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

class Plan(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

class Poliza(models.Model):
    class Estado(models.TextChoices):
        ACTIVA = "ACTIVA", "Activa"
        INACTIVA = "INACTIVA", "Inactiva"
        SUSPENDIDA = "SUSPENDIDA", "Suspendida"

    numero = models.CharField(max_length=100, unique=True)
    asegurado = models.ForeignKey(Asegurado, on_delete=models.PROTECT, related_name='polizas')
    plan =models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='polizas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(choices=Estado.choices, default=Estado.ACTIVA, max_length=20)

class Cobertura(models.Model):
    nombre = models.CharField(max_length=100)

class Consumo(models.Model):
    poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE, related_name='consumo')
    cobertura = models.ForeignKey(Cobertura, on_delete=models.PROTECT, related_name='consumo')
    fecha = models.DateTimeField(auto_now_add=True)

class PlanCobertura(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='plan_cobertura')
    cobertura = models.ForeignKey(Cobertura, on_delete=models.CASCADE, related_name='plan_cobertura')
    limite_usos = models.PositiveIntegerField()

    class Meta:
        unique_together = ('plan', 'cobertura')
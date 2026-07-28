from django.db import models
from django.utils import timezone

class Asegurado(models.Model):
    numero_documento = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombres} - {self.apellidos} - {self.numero_documento}"

class Plan(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

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

    def __str__(self):
        return f"{self.numero} - {self.asegurado.numero_documento}"

    @property
    def esta_vigente(self):
        hoy = timezone.localdate()
        return (
                self.estado == self.Estado.ACTIVA
                and self.fecha_inicio <= hoy <= self.fecha_fin
        )

class Cobertura(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Consumo(models.Model):
    poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE, related_name='consumo')
    cobertura = models.ForeignKey(Cobertura, on_delete=models.PROTECT, related_name='consumo')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poliza.numero} - {self.cobertura.nombre}"

class PlanCobertura(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='plan_cobertura')
    cobertura = models.ForeignKey(Cobertura, on_delete=models.CASCADE, related_name='plan_cobertura')
    limite_usos = models.PositiveIntegerField()

    class Meta:
        unique_together = ('plan', 'cobertura')

    def __str__(self):
        return f"{self.plan.nombre} - {self.cobertura.nombre} - {self.limite_usos}"
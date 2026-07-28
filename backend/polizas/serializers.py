from rest_framework import serializers

from .models import Poliza, Asegurado, Plan

class AseguradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asegurado
        fields = ["numero_documento", "nombres", "apellidos"]

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "nombre", "descripcion"]

class PolizaSerializer(serializers.ModelSerializer):
    asegurado = AseguradoSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)
    esta_vigente =serializers.BooleanField(read_only=True)

    class Meta:
        model = Poliza
        fields = ["id", "numero", "estado", "fecha_inicio", "fecha_fin", "esta_vigente", "asegurado", "plan"]
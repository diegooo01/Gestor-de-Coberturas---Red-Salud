from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Poliza, PlanCobertura, Consumo
from .serializers import PolizaSerializer

@api_view(["GET"])
def consultar_poliza(request, numero):
    try:
        poliza = Poliza.objects.get(numero=numero)
    except Poliza.DoesNotExist:
        return Response({"error": "Póliza no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PolizaSerializer(poliza)
    return Response(serializer.data)

@api_view(["GET"])
def listar_coberturas(request, numero):
    try:
        poliza = Poliza.objects.get(numero=numero)
    except Poliza.DoesNotExist:
        return Response({"error": "Póliza no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    plan_coberturas = PlanCobertura.objects.filter(plan=poliza.plan)

    data = []

    for pc in plan_coberturas:
        consumos_realizados = Consumo.objects.filter(
            poliza=poliza, cobertura=pc.cobertura
        ).count()
        data.append(
            {
                "cobertura_id": pc.cobertura.id,
                "nombre": pc.cobertura.nombre,
                "limite_usos": pc.limite_usos,
                "consumos_realizados": consumos_realizados,
                "saldo_disponible": pc.limite_usos - consumos_realizados,
            }
        )
    return Response(data)
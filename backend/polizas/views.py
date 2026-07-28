from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample

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

@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {"cobertura_id": {"type": "integer"}},
            "required": ["cobertura_id"],
        }
    },
    examples=[
        OpenApiExample("Ejemplo", value={"cobertura_id": 2}),
    ],
)
@api_view(["POST"])
def registrar_consumo(request, numero):
    #Validacion 1: La poliza debe existir
    try:
        poliza = Poliza.objects.get(numero=numero)
    except Poliza.DoesNotExist:
        return Response(
            {"detail": "La póliza no existe."},
            status=status.HTTP_404_NOT_FOUND,
        )

    #Validacion 2: La poliza tiene que estar vigente
    if not poliza.esta_vigente:
        return Response(
            {"detail": "La póliza no está vigente."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    #Se debe indicar la cobertura la cual se quiere registrar el consumo
    cobertura_id = request.data.get("cobertura_id")
    if not cobertura_id:
        return Response(
            {"detail": "Debe indicar la cobertura (cobertura_id)."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    #Validacion 3: La cobertura que se elige debe pertenecer a la poliza
    try:
        plan_cobertura = PlanCobertura.objects.get(
            plan=poliza.plan, cobertura_id=cobertura_id
        )
    except PlanCobertura.DoesNotExist:
        return Response(
            {"detail": "La cobertura no pertenece al plan de la póliza."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    #Validacion 4: No se debe exceder el limite de uso de la cobertura
    consumos_realizados = Consumo.objects.filter(
        poliza=poliza, cobertura_id=cobertura_id
    ).count()
    if consumos_realizados >= plan_cobertura.limite_usos:
        return Response(
            {"detail": "Se alcanzó el límite de usos de esta cobertura."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    #Se crea el consumo/cobertura
    Consumo.objects.create(poliza=poliza, cobertura_id=cobertura_id)

    return Response(
        {
            "detail": "Consumo registrado correctamente.",
            "cobertura": plan_cobertura.cobertura.nombre,
            "consumos_realizados": consumos_realizados + 1,
            "saldo_disponible": plan_cobertura.limite_usos - (consumos_realizados + 1),
        },
        status=status.HTTP_201_CREATED,
    )

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Poliza
from .serializers import PolizaSerializer

@api_view(["GET"])
def consultar_poliza(request, numero):
    try:
        poliza = Poliza.objects.get(numero=numero)
    except Poliza.DoesNotExist:
        return Response({"error": "Póliza no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PolizaSerializer(poliza)
    return Response(serializer.data)
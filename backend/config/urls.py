"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema

class TokenObtainPairDoc(TokenObtainPairView):
    @extend_schema(
        summary="Iniciar sesión",
        description="Devuelve un token de acceso (access) y uno de refresco (refresh).",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshDoc(TokenRefreshView):
    @extend_schema(
        summary="Refrescar token",
        description="Devuelve un nuevo token de acceso a partir del refresh.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("polizas.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/token/", TokenObtainPairDoc.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshDoc.as_view(), name="token_refresh"),
]

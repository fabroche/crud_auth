from django.urls import re_path, include, path
from rest_framework import routers, permissions

from . import views
from .views import PersonaApiView

# para Swagger
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Creando esquema de configuracion para la auto doc de swagger
schema_view = get_schema_view(
    openapi.Info(
        title="SimpleAPI",
        default_version='v1',
        description="Practice API that simuling an Person directory",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="brochegomezf@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = routers.DefaultRouter()

router.register(r'personas', PersonaApiView, basename='persona')

urlpatterns = [
    re_path('api/v1/', include(router.urls)),
    re_path('login', views.login, name='login'),
    re_path('register', views.register, name='register'),
    re_path('profile', views.profile, name='profile'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

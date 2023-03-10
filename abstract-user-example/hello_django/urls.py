from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    # path('users/', include('django.contrib.auth.urls')),
    # re_path('auth/', include('djoser.urls.base')),
    # re_path(r"^auth/", include("djoser.urls.authtoken")),
    re_path('auth/', include('djoser.urls.jwt')),
    # re_path(r"^auth/", include("djoser.social.urls")),
    path('', include('users.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # re_path(r"^auth/", include("djoser.urls.base")),
    # re_path(r"^auth/", include("djoser.urls.authtoken")),
    # re_path(r"^auth/", include("djoser.urls.jwt")),
    # re_path(r"^auth/", include("djoser.social.urls")),
    # re_path(r"^webauthn/", include("djoser.webauthn.urls")),

]

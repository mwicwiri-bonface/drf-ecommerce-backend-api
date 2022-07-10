from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce API",
        default_version='v1',
        description="API endpoints for Ecommerce App. Find all information related to the routes included in "
                    "Ecommerce App under this document. \n\nThe `swagger-ui` view can be found [here](/)."
                    "\n\nThe `ReDoc` view can be found [here](/api/redoc/). ",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mwicwiribonface@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/', include('product.api.urls')),

    # SWAGGER UI patterns
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

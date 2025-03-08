from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define the Bearer token in the OpenAPI schema
auth_scheme = openapi.Parameter(
    'Authorization', openapi.IN_HEADER,
    description="JWT token required to authorize",
    type=openapi.TYPE_STRING,
    required=True  # Marking the token as required
)

# Create the schema view for the Swagger docs
schema_view = get_schema_view(
    openapi.Info(
        title="Poll System API",
        default_version='v1',
        description="API documentation for the Poll System",
        contact=openapi.Contact(email="contact@pollsystem.local"),
    ),
    public=True,
    permission_classes=(AllowAny,),  # Allow any user (public access to docs)
    authentication_classes=(JWTAuthentication,),  # Use JWT for authentication
)

# Define URL patterns
urlpatterns = [
    # Other URLs...
    path('admin/', admin.site.urls),
    path('api/', include('polls.urls')),
    # Swagger Docs URL with Bearer token authorization
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_docs'),
]

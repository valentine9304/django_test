from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from app.views import PageListView, PageDetailView


schema_view = get_schema_view(
    openapi.Info(title="SWAGGER", default_version="v1"),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("pages/", PageListView.as_view(), name="page-list"),
    path("pages/<int:pk>/", PageDetailView.as_view(), name="page-detail"),
]

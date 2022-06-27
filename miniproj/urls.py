"""miniproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from miniproj.api.patient.views import PatientViewset
from miniproj.api.physician.views import PhysicianViewset
from miniproj.api.sample.views import SampleViewset
from miniproj.api.hospital.views import HospitalViewset
from miniproj.api.lab_storage.views import LabStorageViewset
from miniproj.api.order.views import OrderViewset


router = DefaultRouter()
router.register(r"patient", PatientViewset, basename="patient")
router.register(r"physician", PhysicianViewset, basename="physician")
router.register(r"sample", SampleViewset, basename="sample")
router.register(r"hospital", HospitalViewset, basename="hospital")
router.register(r"labstorage", LabStorageViewset, basename="lab_storage")
router.register(r"order", OrderViewset, basename="order")

schema_view = get_schema_view(
    openapi.Info(
        default_version="v1",
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        terms_of_service="https://example.com/",
        contact=openapi.Contact(email="admin@localhost.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(
        r"^api/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^api/swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^api/redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # path("hospital/", views.hospital_list, name="hospital-list"),
    # path("hospital/<int:id>/", views.hospital_details, name="hospital-detail"),
    # path("hospital/remove/<int:id>", views.hospital_remove, name="hospital-detail"),
    # path("hospital/", views.HospitalList.as_view()),
    # path("hospital/<int:id>", views.HospitalDetail.as_view()),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

# urlpatterns = format_suffix_patterns(urlpatterns)

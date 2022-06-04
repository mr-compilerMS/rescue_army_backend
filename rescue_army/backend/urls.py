from django.urls import include, path
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r"events", views.EventViewSet)
router.register(r"resources", views.ResourceViewSet)
router.register(r"volunteers", views.VolunteerViewSet)
urlpatterns = [
    path("", include(router.urls)),
]

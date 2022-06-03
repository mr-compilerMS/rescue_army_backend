from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r"events", views.EventViewSet)
router.register(r"resources", views.ResourceViewSet)

print(router.urls)

urlpatterns = [
    path("", include(router.urls)),
    # path("events/<uuid:id>/", views.event_detail),
]

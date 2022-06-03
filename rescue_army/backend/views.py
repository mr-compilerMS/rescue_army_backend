from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Event, Resource
from .serializers import (
    EventListSerializer,
    EventSerializer,
    ResourceSerializer,
    ResourceListSerializer,
)


class EventViewSet(ReadOnlyModelViewSet):
    queryset = (
        Event.objects.order_by("last_updated")
        .all()
        .prefetch_related("images", "venues")
    )
    serializer_class = EventSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = EventListSerializer
        self.queryset = (
            Event.objects.order_by("last_updated")
            .all()
            .prefetch_related("images", "venues")
        )
        return super().list(request, *args, **kwargs)


class ResourceViewSet(ReadOnlyModelViewSet):
    queryset = (
        Resource.objects.select_related("owner__user").order_by("upload_date").all()
    )
    serializer_class = ResourceSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = ResourceListSerializer
        return super().list(request, *args, **kwargs)

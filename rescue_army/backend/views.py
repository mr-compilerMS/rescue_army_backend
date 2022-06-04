from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from .models import Event, Resource, Volunteer
from .serializers import (
    EventListSerializer,
    EventSerializer,
    ResourceSerializer,
    ResourceListSerializer,
    VolunteerSerializer,
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


class VolunteerViewSet(ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

    @action(detail=False, methods=["GET", "PUT"])
    def me(self, request):
        try:
            volunteer = Volunteer.objects.select_related("address").get(
                user__id=request.user.id
            )
            if request.method == "GET":
                s = VolunteerSerializer(volunteer)
                return Response(s.data)
            elif request.method == "PUT":
                s = VolunteerSerializer(volunteer, data=request.data)
                s.is_valid(raise_exception=True)
                s.save()
                return Response(s.data)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

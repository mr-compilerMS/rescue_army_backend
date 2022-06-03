from turtle import title
import uuid
from rest_framework import serializers


from .models import Event, EventImage, EventVenue, Resource, Staff


class EventImageSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url)

    def get_image_thumbnail(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image_thumbnail.url)

    class Meta:
        model = EventImage
        fields = ["image", "alternative_text", "image_thumbnail"]


class EventVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventVenue
        exclude = ["id", "event"]


class EventListSerializer(serializers.ModelSerializer):
    images = EventImageSerializer(many=True)
    get = serializers.HyperlinkedIdentityField(
        view_name="event-detail", lookup_field="pk"
    )

    class Meta:
        model = Event
        fields = ["id", "title", "start_time", "images", "get"]
        ordering = ["last_updated"]


class EventSerializer(serializers.ModelSerializer):
    images = EventImageSerializer(many=True, read_only=True)
    venues = EventVenueSerializer(many=True, read_only=True)
    type = serializers.CharField(source="get_type_display")

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "organizer",
            "description",
            "start_time",
            "end_time",
            "is_offline",
            "url",
            "type",
            "images",
            "venues",
        ]
        ordering = ["last_updated"]


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["user"]


class ResourceListSerializer(serializers.ModelSerializer):
    get = serializers.HyperlinkedIdentityField(
        view_name="resource-detail", lookup_field="pk"
    )

    class Meta:
        model = Resource
        fields = ["id", "title", "thumbnail", "get"]


class ResourceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.user.__str__")

    class Meta:
        model = Resource
        fields = [
            "id",
            "title",
            "upload_date",
            "description",
            "file",
            "thumbnail",
            "owner",
        ]

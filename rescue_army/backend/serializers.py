from rest_framework import serializers

from .models import Event, EventImage, EventVenue, Resource, Staff, Volunteer, Address


class EventImageSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get("request")
        try:
            if obj.image:
                return request.build_absolute_uri(obj.image.url)
            else:
                return None
        except:
            return None

    def get_image_thumbnail(self, obj):
        request = self.context.get("request")
        try:
            if obj.image_thumbnail:
                return request.build_absolute_uri(obj.image_thumbnail.url)
            else:
                return None
        except Exception as e:
            print(e)
            return None

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
        fields = ["id", "title", "start_time", "images", "get", "is_offline"]
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
    extension = serializers.SerializerMethodField()

    def get_extension(self, obj):
        return obj.extension()

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
            "extension",
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["volunteer"]


class VolunteerSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Volunteer
        fields = ["id", "gender", "birth_date", "type", "user", "address"]
        read_only_fields = ["user"]

    def update(self, instance, validated_data):
        address = validated_data.pop("address")
        addr = Address.objects.get(pk=instance.id)
        address = AddressSerializer(addr, data=address)
        address.is_valid(raise_exception=True)
        address.save()
        instance = super().update(instance, validated_data)
        instance.address = address.instance
        return instance


class UpdateVolunteerSerializer(VolunteerSerializer):
    address = AddressSerializer(read_only=True)

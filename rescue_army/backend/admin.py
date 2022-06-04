import datetime
from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.db.models import F
from django.urls import reverse
from imagekit.admin import AdminThumbnail

from .models import EventVenue, Resource, Volunteer, Staff, Address, Event, EventImage


class VolunteerAddressInline(admin.StackedInline):
    model = Address


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "type",
        "volunteer_city",
        "age",
    )
    list_per_page = 10
    list_select_related = ["user", "address"]

    ordering = ("user__first_name", "user__last_name")
    search_fields = ("user__first_name", "user__last_name")
    list_filter = ("type",)
    autocomplete_fields = ["user"]

    inlines = [VolunteerAddressInline]

    @admin.display()
    def volunteer_city(self, volunteer):
        return volunteer.address.city

    @admin.display(ordering="birth_date")
    def age(self, Volunteer):
        return datetime.date.today().year - Volunteer.birth_date.year


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = ["username", "first_name", "last_name", "city", "state"]
    list_per_page = 10
    # list_select_related = ["volunteer"]
    search_fields = ["first_name", "last_name", "city", "state"]

    @admin.display(ordering="first_name")
    def first_name(self, address):
        return address.first_name

    @admin.display(ordering="last_name")
    def last_name(self, address):
        return address.last_name

    @admin.display(ordering="username")
    def username(self, address):
        return address.username

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                first_name=F("volunteer__user__first_name"),
                last_name=F("volunteer__user__last_name"),
                username=F("volunteer__user__username"),
            )
        )


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "gender",
        "region",
        "designation",
    ]
    list_select_related = ["user"]

    list_per_page = 10

    ordering = ("user__first_name", "user__last_name")
    search_fields = ("user__first_name", "user__last_name")
    autocomplete_fields = ("user",)


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1


class EventVenueInline(admin.StackedInline):
    model = EventVenue
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "start_time", "end_time", "organizer", "images"]
    search_fields = ["title", "organizer", "description"]

    inlines = [EventImageInline, EventVenueInline]

    def images(self, event):
        url = (
            reverse("admin:backend_eventimage_changelist")
            + "?"
            + urlencode({"event__id": str(event.id)})
        )
        return format_html('<a href="{}"><h1>📸</h1></a>', url)


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ["event", "image", "admin_thumbnail"]
    admin_thumbnail = AdminThumbnail(image_field="image_thumbnail")
    autocomplete_fields = ["event"]


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ["title", "upload_date", "file", "resource_thumbnail"]
    resource_thumbnail = AdminThumbnail(image_field="thumbnail")
    search_fields = ["title"]

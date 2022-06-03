from django.contrib import admin

from .models import Volunteer, Address, Event


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "phone")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["volunteer"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title"]

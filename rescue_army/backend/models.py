from django.db import models
from thumbnails.fields import ImageField


class Volunteer(models.Model):

    TYPE_NCC = "N"
    TYPE_NSS = "NS"
    TYPE_STUDENT = "S"
    TYPE_OTHER = "O"

    TYPE_CHOICES = (
        (TYPE_NCC, "NCC"),
        (TYPE_NSS, "NSS"),
        (TYPE_STUDENT, "Student"),
        (TYPE_OTHER, "Other"),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50)
    birth_date = models.DateField()
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=TYPE_NCC)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Staff(models.Model):

    region = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)


class Address(models.Model):
    address_line = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)

    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, primary_key=True
    )


class Event(models.Model):
    title = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255, default="NDRF", blank=True)
    description = models.TextField(blank=True)
    image = ImageField(upload_to="event_images", blank=True)


class Resource(models.Model):
    title = models.CharField(max_length=255)
    upload_date = models.DateField(auto_now=True)
    size = models.FloatField(null=True, blank=True)
    file = models.FileField(upload_to="resources")

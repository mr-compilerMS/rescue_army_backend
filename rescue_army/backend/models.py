import os
from turtle import title
import uuid
from django.conf import settings
from django.db import models

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

GENDER_MALE = "M"
GENDER_FEMALE = "F"
GENDER_CHOICES = ((GENDER_MALE, "Male"), (GENDER_FEMALE, "Female"))


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

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_MALE)
    birth_date = models.DateField()
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=TYPE_NCC)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user}"

    def first_name(self) -> str:
        return self.user.first_name

    def last_name(self) -> str:
        return self.user.last_name

    def username(self) -> str:
        return self.user.username

    class Meta:
        ordering = ["user__first_name", "user__last_name"]


class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_MALE)
    region = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    def first_name(self) -> str:
        return self.user.first_name

    def last_name(self) -> str:
        return self.user.last_name

    def username(self) -> str:
        return self.user.username

    class Meta:
        ordering = ["user__first_name", "user__last_name"]


class Address(models.Model):
    house_no = models.CharField(max_length=255, blank=True, null=True)
    land_mark = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    village = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    alternative_phone = models.CharField(max_length=12, blank=True, null=True)

    volunteer = models.OneToOneField(
        Volunteer, on_delete=models.CASCADE, primary_key=True, related_name="address"
    )

    def __str__(self) -> str:
        return self.volunteer.__str__()


class Event(models.Model):
    EVENT_TYPE_BOOTCAMP = "B"
    EVENT_TYPE_MEETUP = "M"
    EVENT_TYPE_AWARD_CEREMONY = "A"
    EVENT_TYPE_OTHER = "O"
    TYPE_CHOICES = (
        (EVENT_TYPE_BOOTCAMP, "Bootcamp"),
        (EVENT_TYPE_MEETUP, "Meetup"),
        (EVENT_TYPE_AWARD_CEREMONY, "Award Ceremony"),
        (EVENT_TYPE_OTHER, "Other"),
    )

    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_offline = models.BooleanField(default=False)
    url = models.URLField(max_length=255, blank=True, null=True)
    organizer = models.CharField(max_length=255, default="NDRF", blank=True)
    description = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    type = models.CharField(
        max_length=1, choices=TYPE_CHOICES, default=EVENT_TYPE_OTHER
    )

    def __str__(self) -> str:
        return self.title


class EventVenue(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="venues")
    land_mark = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    village = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.event.__str__() + " " + self.land_mark + ", " + self.city


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images/events", blank=True)
    alternative_text = models.CharField(max_length=255, default="Event")
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(100, 50)],
        format="JPEG",
        options={"quality": 60},
    )

    def delete(self, *args, **kwargs):
        try:
            file1 = self.image.path
            file2 = self.image_thumbnail.path
            lst = [file1, file2]  # put file1 and file2 in list
        except:
            pass
        else:
            for path in lst:
                os.remove(path)
        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.event.__str__() + " " + self.id.__str__()


class Resource(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    title = models.CharField(max_length=255)
    upload_date = models.DateField(auto_now=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="files/resources")
    thumbnail = ProcessedImageField(
        upload_to="files/resources/cache",
        processors=[ResizeToFill(100, 60)],
        format="JPEG",
        options={"quality": 80},
    )
    owner = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    def delete(self):
        try:
            file1 = self.file.path
            file2 = self.thumbnail.path
            lst = [file1, file2]  # put file1 and file2 in list
        except:
            pass
        else:
            for path in lst:
                os.remove(path)
        super().delete()

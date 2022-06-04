import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from .managers import UserManager

# Create your models here.


class User(AbstractUser):
    phone_validator = RegexValidator(
        regex=r"^\+?1?\d{9,12}$",
        message="Phone number must be entered in the format: '+91XXXXXXXXXX'.",
    )

    phone = models.CharField(
        max_length=20,
        help_text=_("Phone number must be entered in the format: '+91XXXXXXXXXX'."),
        unique=True,
        validators=[phone_validator],
        error_messages={
            "unique": _("A user with same phone number already exists."),
        },
    )

    avatar = models.ImageField(upload_to="images/avatars", blank=True)
    avatar_thumbnail = ImageSpecField(
        source="avatar",
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 60},
    )

    manger = UserManager()

    def __str__(self) -> str:
        # return ""
        return f"{self.first_name} {self.last_name}"

    def delete(self, *args, **kwargs):
        try:
            file1 = self.avatar.path
            file2 = self.avatar_thumbnail.path
            lst = [file1, file2]  # put file1 and file2 in list
        except:
            pass
        else:
            for path in lst:
                os.remove(path)
        super().delete(*args, **kwargs)

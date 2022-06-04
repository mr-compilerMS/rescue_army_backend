from django.contrib.auth.models import UserManager as BaseUserManager
from django.db.models import Q


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        data = self.get(
            Q(email__iexact=username)
            | Q(username__iexact=username)
            | Q(phone__iexact=username)
        )
        return data

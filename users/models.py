# from django.contrib.auth.forms import UsernameField

# from django.db import models
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# class CustomAccountManager(BaseUserManager):

#     def create_user(self, username, email, is_hospital,  password, **other_fields):
#         if not username:
#             raise ValueError(_("You must provide a username"))
#         if not email:
#             raise ValueError(_("You must provide a email"))

#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, is_hospital= is_hospital **other_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, username, email, is_hospital, password, **other_fields):

#         other_fields.setdefault('is_staff', True)
#         other_fields.setdefault('is_superuser', True)
#         other_fields.setdefault('is_active', True)

#         if other_fields.get('is_staff') is not True:
#             raise ValueError(
#                 "Superuser must be assigned to is_staff = True.")

#         if other_fields.get('is_superuser') is not True:
#             raise ValueError(
#                 "Superuser must be assigned to is_superuser = True.")
        
#         return self.create_user(username, email, is_hospital, password, **other_fields)


# class NewUser(AbstractBaseUser, PermissionsMixin):

#     username = models.CharField(max_length=150, unique=True),
#     email = models.EmailField(_("email address"), unique=True),
#     is_hospital = models.BooleanField(default=True),
#     start_date = models.DateTimeField(default=timezone.now)
#     about = models.TextField(_('about'), max_length=150, blank=True),
#     is_staff = models.BooleanField(default=True),
#     is_active = models.BooleanField(default=True)

#     objects = CustomAccountManager()

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email', 'is_hospital']

#     def __str__(self):
#         return self.username

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager




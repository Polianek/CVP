from datetime import datetime, timezone, timedelta
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.cache import cache
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ponytoon.validators import validate_file_size

class Species(models.Model):
    species_name = models.CharField(max_length=255)

    def __str__(self):
        return self.species_name

class TimeZone(models.Model):
    zone = models.CharField(max_length=100)
    pyzone =  models.CharField(max_length=100)
    def __str__(self):
        return self.zone
    def timezone_dj(self):
        return self.pyzone

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_active=False, is_staff=False, is_admin=False, is_premium=False, is_still_premium=datetime.now(timezone.utc), **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        now = datetime.now(timezone.utc)
        user_obj = self.model(email=self.normalize_email(email), last_login=now, date_joined=now, **extra_fields)
        user_obj.username = username
        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.premium = is_premium
        user_obj.premium_date = is_still_premium
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, username, email, password=None):
        user = self.create_user(username, email, password=password, is_active=True, is_staff=True)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password=password, is_active=True, is_staff=True, is_admin=True)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=35, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    premium = models.BooleanField(default=False) #auto_now_add=True
    premium_date = models.DateTimeField(null=True, blank=True) #, default=timezone.now() #default=datetime.datetime.now()
    # last_seen = models.DateTimeField(null=True, blank=True)
    online = models.IntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    # avatar = models.URLField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to='avatars', validators=[validate_file_size], default='avatars/profile.png')
    species = models.ForeignKey(Species, on_delete=models.CASCADE, null=True, blank=True) #Klucz (species_id)=(1) nie występuje w tabeli "accounts_speces" - po prostu usuń default tu i w pliku migracji
    reputation = models.IntegerField(default=0)
    timezone = models.ForeignKey(TimeZone, on_delete=models.CASCADE, default='16')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_premium(self):
        return self.premium

    @property
    def is_still_premium(self):
        premium_expiration = datetime.now(timezone.utc) + timedelta(days=30)
        if datetime.now(timezone.utc) < self.premium_expiration:
            return self.premium_date
        return

    objects = UserManager()

    @property
    def get_last_seen(self):
        return cache.get('seen_%s' % self.username)

    @property
    def get_online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                         seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

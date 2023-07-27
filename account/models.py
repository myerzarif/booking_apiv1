"""Models of Account App"""
from datetime import timedelta
import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.db import models
from common.models import BaseModel
from django.contrib.auth.models import BaseUserManager, UserManager
from django.utils.translation import gettext_lazy


class Access(BaseModel):
    """
    Access Table
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)


class Role(BaseModel):
    """
    Role Table
    """

    accesses = models.ManyToManyField(Access, blank=True, related_name="access_roles")
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.active = True
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        user = self._create_user(email, password, **extra_fields)
        user.email_verified = True
        user.status = User.UserStatus.ACTIVE
        user.role = User.UserRole.TECH
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    User Table
    """
    objects = CustomUserManager()

    class UserRole(models.TextChoices):
        # Actual value ↓      # ↓ Displayed on Django Admin
        TECH = 'Tech', gettext_lazy('TECH')
        ADMIN = 'Admin', gettext_lazy('ADMIN')
        STAFF = 'Staff', gettext_lazy('STAFF')
    
    class UserStatus(models.TextChoices):
        # Actual value ↓      # ↓ Displayed on Django Admin
        INACTIVE = 'Inactive', gettext_lazy('INACTIVE')
        ACTIVE = 'Active', gettext_lazy('ACTIVE')
        BLOCKED = 'Blocked', gettext_lazy('BLOCKED')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=200, unique=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    job_title = models.CharField(max_length=200, blank=True, null=True)
    roles = models.ManyToManyField(Role, blank=True, related_name="role_users")
 
    created_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    role = models.CharField(
        max_length=15,
        choices=UserRole.choices,
        default=UserRole.STAFF,
    )
    status = models.CharField(
        max_length=15,
        choices=UserStatus.choices,
        default=UserStatus.INACTIVE,
    )

    USERNAME_FIELD = "email"
    EmailField = "email"
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Users"
        verbose_name = "User"

class AccessToken(Token):
    """
    Authorization Token Model
    """

    def expire_time_func():
        return timezone.now() + timedelta(seconds=settings.TOKEN_AUTH_EXPIRED_TIME)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    expire_time = models.DateTimeField(default=expire_time_func)
    is_active = models.BooleanField(default=True)
    # Hash of user agent request -> Default is hash of b''
    user_agent = models.CharField(max_length=150,
                                  default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    #
    origin = models.CharField(
        max_length=200, default="https://matna.pnete.com")
    created_at = models.DateTimeField(
        default=timezone.now)
    last_modified = models.DateTimeField(
        auto_now=True)

    created_by = models.ForeignKey(
        "account.User",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL
    )

    modified_by = models.ForeignKey(
        "account.User",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL
    )

    def isExpire(self):
        now = timezone.now()
        if self.expire_time <= now:
            return True
        if settings.EXPIRE_TOKEN_WHEN_USER_ACTIVE:
            if now - self.created_at >= timedelta(days=settings.TOKEN_AUTH_EXPIRED_TIME):
                return True
        if not self.is_active:
            return True
        return False

    def update(self):
        self.expire_time = timezone.now() + timedelta(seconds=settings.TOKEN_AUTH_EXPIRED_TIME)
        self.save()

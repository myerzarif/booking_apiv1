"""Models of Hotel App"""
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
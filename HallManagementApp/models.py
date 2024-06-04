from email.policy import default
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum
from django.db import models
from django_enum_choices.fields import EnumChoiceField
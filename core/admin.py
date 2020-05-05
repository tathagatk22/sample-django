# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from core.models import CustomUser, ActivityPeriods

admin.site.register(CustomUser)  # Registering CustomUser Models with admin
admin.site.register(ActivityPeriods)  # Registering ActivityPeriod Models with admin

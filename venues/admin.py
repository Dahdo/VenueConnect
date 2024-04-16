from django.contrib import admin
from venues.models import Venue
from django.contrib.auth.admin import UserAdmin

admin.site.register(Venue)
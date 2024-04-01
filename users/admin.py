from django.contrib import admin
from users.models import PhoneNumber, CustomUser, Profile
from django.contrib.auth.admin import UserAdmin

admin.site.register(PhoneNumber)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Profile)
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

class PhoneNumber(models.Model):
    number = PhoneNumberField(unique=True)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.phone_number.as_e164

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.OneToOneField(PhoneNumber, related_name="user", on_delete=models.CASCADE, blank=True, null=True)

    # provide unique relate_name for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='custom_group', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_permissions', blank=True)

    def __str__(self):
        return f"user: @{self.username}"
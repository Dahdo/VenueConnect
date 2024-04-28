from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
import os

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)

    # provide unique relate_name for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='custom_group', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_permissions', blank=True)

    def __str__(self):
        return f"user: @{self.username}"


def avatar_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.user.username}.{ext}"
    return os.path.join('avatars', filename)

class Profile(models.Model):
    LANGUAGES_SPOKEN = [
        ('en', 'English'),
        ('pl', 'Polish'),
        ('de', 'German'),
        ('fr', 'French'),
    ]
    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_upload_to, blank=True, null=True)
    languages_spoken = models.CharField(max_length=20, choices=LANGUAGES_SPOKEN, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
    
    def __str__(self):
        return f"profile: @{self.user.username}"

    # Signal to create a UserProfile instance once a CustomUser instance is created
    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
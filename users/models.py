from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class Address(models.Model):
    country = CountryField()
    city = models.CharField(max_length=100, blank=False, null=False)
    street = models.CharField(max_length=100, blank=False, null=False)
    apartment = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()
    

class PhoneNumber(models.Model):
    phone_number = PhoneNumberField(unique=True)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.phone_number.as_e164

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    date_of_birth = models.DateField()
    phone_number = models.OneToOneField(PhoneNumber, related_name="user", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, related_name='user', on_delete=models.SET_NULL, null=True)

    # provide unique relate_name for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='custom_group')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_permissions')

    def __str__(self):
        return f"user: {self.get_full_name} @{self.username}"


class Profile(models.Model):
    LANGUAGES_SPOKEN = [
        ('en', 'English'),
        ('pl', 'Polish'),
        ('de', 'German'),
        ('fr', 'French'),
    ]
    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar', blank=True, null=True)
    languages_spoken = models.CharField(max_length=20, choices=LANGUAGES_SPOKEN, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
    
    def __str__(self):
        return f"profile: {self.user.get_full_name} @{self.username}"

    @property
    def profile_pic_url(self):
        try:
            url = self.profile_pic.url
        except:
            url = ''
        return url

    # Signal to create a UserProfile instance once a CustomUser instance is created
    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

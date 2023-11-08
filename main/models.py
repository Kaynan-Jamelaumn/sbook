from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    GENDER_CHOICES = [
        ('Woman', 'Woman'),
        ('Man', 'Man'),
        ('Non-binary', 'Non-binary'),
        ('Other', 'Other'),
        ('Genderfluid', 'Genderfluid'),
        ('Agender', 'Agender'),
        ('The Love of Your Life', 'The Love of Your Life'),
        ('Heavenly Demon', 'Heavenly Demon'),
    ]
    sex = models.CharField(
        max_length=6, choices=SEX_CHOICES, null=True, blank=True)
    gender = models.CharField(
        max_length=30, choices=GENDER_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    pseudo_name = models.CharField(
        max_length=150, null=False, blank=False, unique=True)
    groups = models.ManyToManyField(
        'auth.Group', related_name='custom_users', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='custom_users')

    def __str__(self):
        return self.username


class Author(models.Model):
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)

    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True)

    bio = models.TextField(null=True, blank=True, max_length=3000)

    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    GENDER_CHOICES = [
        ('Woman', 'Woman'),
        ('Man', 'Man'),
        ('Non-binary', 'Non-binary'),
        ('Other', 'Other'),
        ('Genderfluid', 'Genderfluid'),
        ('Agender', 'Agender'),
        ('The Love of Your Life', 'The Love of Your Life'),
        ('Heavenly Demon', 'Heavenly Demon'),
    ]
    sex = models.CharField(
        max_length=6, choices=SEX_CHOICES, null=True, blank=True)
    gender = models.CharField(
        max_length=30, choices=GENDER_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    pseudo_name = models.CharField(
        max_length=150, null=True, blank=True)
    death_day = models.DateField(null=True, blank=True)
    home_country = models.CharField(
        max_length=150, null=True, blank=True)
    home_state = models.CharField(
        max_length=150, null=True, blank=True)
    home_town = models.CharField(
        max_length=150, null=True, blank=True)

    def __str__(self):
        return f" {self.pseudo_name} {self.first_name} {self.last_name}"

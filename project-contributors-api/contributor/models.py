from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

from django_countries.fields import CountryField

from common.models.base import BaseModel


class Contributor(BaseModel, AbstractUser):
    # 'username', 'first_name' and 'last_name' are inherited from AbstractUser

    email = models.EmailField(unique=True)
    birth_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),  # Minimum allowed year
            MaxValueValidator(datetime.now().year),  # Current year + 10 years
        ]
    )
    address = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField()

    def __str__(self):
        return f"{self.username} {self.email}"

class ContributorSkillset(BaseModel):
    LANGUAGE_CHOICES = [
        ('PY', 'Python'),
        ('JS', 'JavaScript'),
        ('JAVA', 'Java'),
        ('CPP', 'C++'),
        ('GO', 'Go'),
        ('RS', 'Rust'),
        ('LUA', 'LUA'),
        ('JL', 'Julia'),
    ]

    EXPERIENCE_CHOICES = [
        ('BEG', 'Beginner'),
        ('EXD', 'Experienced'),
        ('EXP', 'Expert'),
    ]

    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)

    programming_language = models.CharField(
        max_length=8,
        choices=LANGUAGE_CHOICES
    )

    experience_level = models.CharField(
        max_length=3,
        choices=EXPERIENCE_CHOICES
    )

    class Meta:
        unique_together = ['contributor', 'programming_language']



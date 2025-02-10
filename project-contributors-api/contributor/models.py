from django.contrib.auth.models import AbstractUser
from django.db import models

from rest_framework.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

from django_countries.fields import CountryField

from common.models.base import BaseModel


class Contributor(BaseModel, AbstractUser):
    # 'username' is inherited from AbstractUser

    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),  # Minimum allowed year
            MaxValueValidator(datetime.now().year),  # Current year + 10 years
        ]
    )
    address = models.CharField(max_length=100, blank=True, null=True)
    country_code = CountryField()

    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",
        "birth_year",
        "address",
        "country_code",
    ]

    def __str__(self):
        return f"{self.username} {self.email}"


class ContributorSkillset(BaseModel):
    LANGUAGE_CHOICES = [
        ("PY", "Python"),
        ("JS", "Javascript"),
        ("JAVA", "Java"),
        ("CPP", "C++"),
        ("GO", "Go"),
        ("RS", "Rust"),
        ("LUA", "Lua"),
        ("JL", "Julia"),
    ]

    EXPERIENCE_CHOICES = [
        ("BEG", "Beginner"),
        ("EXD", "Experienced"),
        ("EXP", "Expert"),
    ]

    contributor = models.ForeignKey(
        Contributor, on_delete=models.CASCADE, related_name="skillset"
    )
    programming_language = models.CharField(
        max_length=8, choices=LANGUAGE_CHOICES, blank=False, null=False
    )
    experience_level = models.CharField(
        max_length=3, choices=EXPERIENCE_CHOICES, blank=False, null=False
    )

    class Meta:
        unique_together = ["contributor", "programming_language"]

    def clean(self):
        """
        Normally DRF should invoke is method during .is_valid() and get Django's ValidationError exception.
        Since this does not happen, DRF's ValidationError is 'thrown' from here directly.
        """
        # Check if the Contributor has already skillset in speicifc programming language
        if ContributorSkillset.objects.filter(
            contributor=self.contributor, programming_language=self.programming_language
        ).exists():
            raise ValidationError(
                {
                    "error": f"Contributor is already skilled in {self.get_programming_language_display()}."
                }
            )

        # Check if the Contributor already has 3 skillsets
        if (
            ContributorSkillset.objects.filter(contributor=self.contributor).count()
            >= 3
        ):
            raise ValidationError({"error": "A Contributor can have at most 3 skills."})

    def save(self, *args, **kwargs):
        self.clean()  # Call the custom clean method before saving
        super().save(*args, **kwargs)

    @classmethod
    def get_programming_language_key(cls, display_value):
        choices = dict(cls.LANGUAGE_CHOICES)
        choices = {v: k for k, v in choices.items()}  # Reverse dict
        return choices.get(display_value, None)

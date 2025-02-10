from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from datetime import datetime

from allauth.account.adapter import get_adapter

from django.contrib.auth import get_user_model

from .models import Contributor, ContributorSkillset


class ContributorRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=Contributor.objects.all())]
    )
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    birth_year = serializers.IntegerField(
        required=True,
        validators=[
            MinValueValidator(1900),  # Minimum allowed year
            MaxValueValidator(
                datetime.now().year
            ),  # Maximum allowed year (current year)
        ],
    )
    address = serializers.CharField(max_length=100, required=False, allow_blank=True)
    country_code = serializers.CharField(max_length=3, required=True)

    def get_cleaned_data(self):
        super(ContributorRegisterSerializer, self).get_cleaned_data()
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "birth_year": self.validated_data.get("birth_year", ""),
            "address": self.validated_data.get("address", ""),
            "country_code": self.validated_data.get("country_code", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        user.username = self.cleaned_data.get("username")
        user.email = self.cleaned_data.get("email")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.birth_year = self.cleaned_data.get("birth_year")
        user.address = self.cleaned_data.get("address")
        user.country_code = self.cleaned_data.get("country_code")
        user.set_password(self.cleaned_data.get("password1"))

        adapter.save_user(request, user, self)
        return user


class ContributorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "birth_year",
            "country_code",
            "address",
        ]


class ContributorSkillsetSerializer(serializers.ModelSerializer):
    programming_language = serializers.CharField()
    experience_level = serializers.CharField()

    class Meta:
        model = ContributorSkillset
        fields = [
            "programming_language",
            "experience_level",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if "programming_language" in representation:
            representation["programming_language"] = (
                instance.get_programming_language_display()
            )
        if "experience_level" in representation:
            representation["experience_level"] = instance.get_experience_level_display()

        return representation

    def to_internal_value(self, data):
        data = data.copy()

        if "programming_language" in data:
            choices = dict(ContributorSkillset.LANGUAGE_CHOICES)
            choices = {v: k for k, v in choices.items()}  # Reverse dict
            data["programming_language"] = choices.get(data["programming_language"])

        if "experience_level" in data:
            choices = dict(ContributorSkillset.EXPERIENCE_CHOICES)
            choices = {v: k for k, v in choices.items()}  # Reverse dict
            data["experience_level"] = choices.get(data["experience_level"])

        return super().to_internal_value(data)

    def validate_programming_language(self, value):
        contributor = self.context.get("contributor")
        programming_language_choice = ContributorSkillset.get_programming_language_key(
            value
        )

        if ContributorSkillset.objects.filter(
            contributor=contributor, programming_language=programming_language_choice
        ).exists():
            raise ValidationError(
                f"Contributor is already skilled in {value}."
            )
        return value

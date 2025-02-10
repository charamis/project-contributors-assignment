from django.urls import path
from .views import contributor_skills

urlpatterns = [
    path("skills/", contributor_skills),
]

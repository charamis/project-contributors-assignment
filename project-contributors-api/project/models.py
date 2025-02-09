from django.db import models

from django.core.validators import MaxValueValidator

from common.models.base import BaseModel
from contributor.models import Contributor


class Project(BaseModel):
    STATUS_CHOICES = [
        ("NOT_STARTED", "Not Started"),
        ("COMPLETED", "Completed"),
        ("ONGOING", "Ongoing"),
        ("PAUSED", "Paused"),
        ("ARCHIVED", "Archived"),
    ]

    contributors = models.ManyToManyField(Contributor, related_name="projects")
    name = models.CharField(max_length=50)
    description = models.TextField()
    maximum_contributors = models.PositiveIntegerField(
        validators=[MaxValueValidator(3)]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class ContributionRequest(BaseModel):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("DISMISSED", "Dismissed"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "contributor"],
                name="unique_project_contributor_when_request_pending",
                condition=models.Q(
                    status="PENDING"
                ),  # A Contributor can have at most one Pending ContributionRequest to a Project
            )
        ]

    def __str__(self):
        return f"{self.project} - {self.contributor} - {self.status}"

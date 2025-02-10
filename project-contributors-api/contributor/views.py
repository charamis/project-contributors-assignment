from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Contributor, ContributorSkillset
from .serializers import ContributorSkillsetSerializer


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def contributor_skills(request):
    contributor = request.user

    if request.method == "GET":
        serializer = ContributorSkillsetSerializer(contributor.skillset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ContributorSkillsetSerializer(data=request.data)

        if contributor.skillset.count() >= 3:
            return Response(
                {"error": "A Contributor can have at most 3 skills."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            serializer.save(contributor=contributor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        programming_language = request.data.get("programming_language")

        if not programming_language:
            return Response(
                {"error": "Programming language parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get programming language system code
        programming_language_choice = ContributorSkillset.get_programming_language_key(
            programming_language
        )

        try:
            skillset = ContributorSkillset.objects.get(
                contributor=contributor,
                programming_language=programming_language_choice,
            )
            skillset.delete()
            return Response(
                {"message": "Skill removed."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except ContributorSkillset.DoesNotExist:
            return Response(
                {"error": "Skill not found for this Contributor."},
                status=status.HTTP_404_NOT_FOUND,
            )

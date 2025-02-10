import pytest
from rest_framework import status
from rest_framework.test import APIClient
from .models import Contributor, ContributorSkillset


@pytest.fixture
def contributor():
    return Contributor.objects.create_user(
        username="test_contributor",
        email="test@example.com",
        password="testpassword123",
        first_name="Test",
        last_name="Contributor",
        birth_year=1990,
        address="Test Address",
        country_code="US",
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_skill(contributor):
    # Helper function to create a skillset
    def _create_skill(language, experience):
        return ContributorSkillset.objects.create(
            contributor=contributor,
            programming_language=language,
            experience_level=experience,
        )

    return _create_skill


@pytest.mark.django_db
def test_get_contributor_skills(api_client, contributor, create_skill):
    create_skill("PY", "BEG")
    create_skill("JS", "EXD")

    access_token = api_client.post(
        "/api/v1/auth/login/",
        {"username": "test_contributor", "password": "testpassword123"},
    ).data.get("access")

    # Get the skills of the contributor
    response = api_client.get(
        f"/api/v1/contributor/skills/",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["programming_language"] == "Python"
    assert response.data[1]["programming_language"] == "Javascript"
    assert response.data[0]["experience_level"] == "Beginner"
    assert response.data[1]["experience_level"] == "Experienced"


@pytest.mark.django_db
def test_add_contributor_skill(api_client, contributor, create_skill):
    access_token = api_client.post(
        "/api/v1/auth/login/",
        {"username": "test_contributor", "password": "testpassword123"},
    ).data.get("access")

    skill_data = {"programming_language": "Java", "experience_level": "Beginner"}
    response = api_client.post(
        f"/api/v1/contributor/skills/",
        skill_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["programming_language"] == "Java"
    assert response.data["experience_level"] == "Beginner"


@pytest.mark.django_db
def test_add_duplicate_skill(api_client, contributor, create_skill):
    create_skill("PY", "EXD")

    access_token = api_client.post(
        "/api/v1/auth/login/",
        {"username": "test_contributor", "password": "testpassword123"},
    ).data.get("access")

    # Try adding a duplicate skill
    skill_data = {"programming_language": "Python", "experience_level": "Experienced"}
    response = api_client.post(
        f"/api/v1/contributor/skills/",
        skill_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Contributor is already skilled in Python."


@pytest.mark.django_db
def test_add_skill_when_limit_reached(api_client, contributor, create_skill):
    create_skill("PY", "BEG")
    create_skill("JS", "EXD")
    create_skill("JAVA", "EXP")

    access_token = api_client.post(
        "/api/v1/auth/login/",
        {"username": "test_contributor", "password": "testpassword123"},
    ).data.get("access")

    # Try adding a 4th skill (limit exceeded)
    skill_data = {"programming_language": "Go", "experience_level": "Beginner"}
    response = api_client.post(
        f"/api/v1/contributor/skills/",
        skill_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "A Contributor can have at most 3 skills."


@pytest.mark.django_db
def test_delete_contributor_skill(api_client, contributor, create_skill):
    skill = create_skill("PY", "EXD")

    access_token = api_client.post(
        "/api/v1/auth/login/",
        {"username": "test_contributor", "password": "testpassword123"},
    ).data.get("access")

    skill_data = {"programming_language": "Python"}
    response = api_client.delete(
        f"/api/v1/contributor/skills/",
        skill_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not ContributorSkillset.objects.filter(uuid=skill.uuid).exists()


@pytest.mark.django_db
def test_delete_skill_not_found(api_client, contributor):
    access_token = api_client.post(
        "/api/v1/auth/login/",
        {"username": "test_contributor", "password": "testpassword123"},
    ).data.get("access")

    # Try to delete a non-existing skill
    skill_data = {"programming_language": "Lua"}
    response = api_client.delete(
        f"/api/v1/contributor/skills/",
        skill_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "Skill not found for this Contributor."


@pytest.mark.django_db
def test_login_logout(api_client, contributor):
    login_data = {"username": "test_contributor", "password": "testpassword123"}
    login_response = api_client.post("/api/v1/auth/login/", login_data)
    assert login_response.status_code == status.HTTP_200_OK

    access_token = login_response.data.get("access")
    refresh_token = login_response.data.get("refresh")
    assert access_token is not None
    assert refresh_token is not None

    # Call a protected endpoint to verify the user is authenticated
    response = api_client.get(
        f"/api/v1/contributor/skills/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    logout_data = {"refresh": refresh_token}
    logout_response = api_client.post("/api/v1/auth/logout/", logout_data)
    assert logout_response.status_code == status.HTTP_200_OK

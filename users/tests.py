import pytest
from django.urls import reverse
from users.models import Cook
from users.forms import CookCreationForm, CookExperienceUpdateForm


@pytest.mark.django_db
def test_cook_str_and_experience():
    cook = Cook.objects.create_user(
        username="chef1",
        password="test12345",
        first_name="John",
        last_name="Doe",
        years_of_experience=5,
    )
    assert "chef1" in str(cook)
    assert cook.years_of_experience == 5


@pytest.mark.django_db
def test_cook_creation_form_valid():
    form = CookCreationForm(
        data={
            "username": "chef2",
            "first_name": "Anna",
            "last_name": "Smith",
            "years_of_experience": 3,
            "password1": "strongPass123",
            "password2": "strongPass123",
        }
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_cook_experience_update_form_valid():
    cook = Cook.objects.create_user(username="chef3", password="test12345", years_of_experience=1)
    form = CookExperienceUpdateForm(data={"years_of_experience": 10}, instance=cook)
    assert form.is_valid()
    updated_cook = form.save()
    assert updated_cook.years_of_experience == 10


@pytest.mark.django_db
def test_cook_list_view(client):
    Cook.objects.create_user(username="chef4", password="test12345")
    client.login(username="chef4", password="test12345")
    url = reverse("users:cook-list")
    response = client.get(url)
    assert response.status_code == 200
    assert "cook_list" in response.context


@pytest.mark.django_db
def test_cook_create_update_delete_views(client):
    client_user = Cook.objects.create_user(username="admin", password="test12345")
    client.login(username="admin", password="test12345")

    create_url = reverse("users:cook-create")
    response = client.post(
        create_url,
        data={
            "username": "new_cook",
            "first_name": "Jane",
            "last_name": "Smith",
            "years_of_experience": 2,
            "password1": "newpass123",
            "password2": "newpass123",
        },
    )
    assert response.status_code == 302
    cook = Cook.objects.get(username="new_cook")

    update_url = reverse("users:cook-update", args=[cook.id])
    response = client.post(update_url, data={"years_of_experience": 7})
    cook.refresh_from_db()
    assert response.status_code == 302
    assert cook.years_of_experience == 7

    delete_url = reverse("users:cook-delete", args=[cook.id])
    response = client.post(delete_url)
    assert response.status_code == 302
    assert not Cook.objects.filter(id=cook.id).exists()


@pytest.mark.django_db
def test_cook_list_view_with_search(client):
    cook1 = Cook.objects.create_user(username="chef5", password="test12345")
    Cook.objects.create_user(username="othercook", password="test12345")

    client.login(username="chef5", password="test12345")

    url = reverse("users:cook-list")
    response = client.get(url, {"username": "chef5"})

    assert response.status_code == 200
    cook_list = response.context["cook_list"]
    assert len(cook_list) == 1
    assert cook_list[0].username == "chef5"

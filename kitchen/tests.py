import pytest
from django.urls import reverse
from kitchen.models import DishType, Dish, Ingredient
from kitchen.forms import DishForm
from users.models import Cook


@pytest.mark.django_db
def test_dish_type_str():
    dish_type = DishType.objects.create(name="Salad")
    assert str(dish_type) == "Salad"


@pytest.mark.django_db
def test_ingredient_str():
    ingredient = Ingredient.objects.create(name="Tomato")
    assert str(ingredient) == "Tomato"


@pytest.mark.django_db
def test_dish_creation_and_relations():
    cook = Cook.objects.create_user(username="chef", password="test12345")
    dish_type = DishType.objects.create(name="Soup")
    ingredient = Ingredient.objects.create(name="Potato")

    dish = Dish.objects.create(
        name="Borscht",
        description="Beetroot soup",
        price=12.50,
        dish_type=dish_type,
    )
    dish.cooks.add(cook)
    dish.ingredients.add(ingredient)

    assert str(dish) == "Borscht"
    assert cook in dish.cooks.all()
    assert ingredient in dish.ingredients.all()


@pytest.mark.django_db
def test_dish_form_valid():
    dish_type = DishType.objects.create(name="Dessert")
    form = DishForm(
        data={
            "name": "Cake",
            "description": "Sweet cake",
            "price": "5.50",
            "dish_type": dish_type.id,
        }
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_index_view(client):
    cook = Cook.objects.create_user(username="chef", password="test12345")
    client.login(username="chef", password="test12345")
    url = reverse("kitchen:index")
    response = client.get(url)
    assert response.status_code == 200
    assert "num_dishes" in response.context


@pytest.mark.django_db
def test_dish_list_view(client):
    cook = Cook.objects.create_user(username="chef", password="test12345")
    client.login(username="chef", password="test12345")
    dish_type = DishType.objects.create(name="Pizza")
    Dish.objects.create(name="Margarita", description="Classic", price=8.00, dish_type=dish_type)

    url = reverse("kitchen:dish-list")
    response = client.get(url)
    assert response.status_code == 200
    assert "dish_list" in response.context


@pytest.mark.django_db
def test_dish_create_update_delete_views(client):
    cook = Cook.objects.create_user(username="chef", password="test12345")
    client.login(username="chef", password="test12345")
    dish_type = DishType.objects.create(name="Soup")

    create_url = reverse("kitchen:dish-create")
    response = client.post(
        create_url,
        data={"name": "Borscht", "description": "Tasty", "price": 10, "dish_type": dish_type.id},
    )
    assert response.status_code == 302
    dish = Dish.objects.get(name="Borscht")

    update_url = reverse("kitchen:dish-update", args=[dish.id])
    response = client.post(
        update_url,
        data={"name": "Updated Borscht", "description": "Tasty", "price": 12, "dish_type": dish_type.id},
    )
    dish.refresh_from_db()
    assert response.status_code == 302
    assert dish.name == "Updated Borscht"

    delete_url = reverse("kitchen:dish-delete", args=[dish.id])
    response = client.post(delete_url)
    assert response.status_code == 302
    assert not Dish.objects.filter(id=dish.id).exists()


@pytest.mark.django_db
def test_dish_list_view_with_search(client):
    cook = Cook.objects.create_user(username="chef", password="test12345")
    client.login(username="chef", password="test12345")

    dish_type = DishType.objects.create(name="Pizza")
    Dish.objects.create(name="Margarita", description="Classic", price=8.00, dish_type=dish_type)
    Dish.objects.create(name="Pepperoni", description="Spicy", price=9.50, dish_type=dish_type)

    url = reverse("kitchen:dish-list")
    response = client.get(url, {"name": "Margarita"})

    assert response.status_code == 200
    dish_list = response.context["dish_list"]
    assert len(dish_list) == 1
    assert dish_list[0].name == "Margarita"


@pytest.mark.django_db
def test_dishtype_list_view_with_search(client):
    cook = Cook.objects.create_user(username="chef", password="test12345")
    client.login(username="chef", password="test12345")

    DishType.objects.create(name="Soup")
    DishType.objects.create(name="Salad")

    url = reverse("kitchen:dishtype-list")
    response = client.get(url, {"name": "Soup"})

    assert response.status_code == 200
    types = response.context["dishtype_list"]
    assert len(types) == 1
    assert types[0].name == "Soup"


@pytest.mark.django_db
def test_ingredient_list_view_with_search(client):
    cook = Cook.objects.create_user(username="chef", password="test12345")
    client.login(username="chef", password="test12345")

    Ingredient.objects.create(name="Tomato")
    Ingredient.objects.create(name="Potato")

    url = reverse("kitchen:ingredient-list")
    response = client.get(url, {"name": "Tomato"})

    assert response.status_code == 200
    ingredients = response.context["ingredient_list"]
    assert len(ingredients) == 1
    assert ingredients[0].name == "Tomato"

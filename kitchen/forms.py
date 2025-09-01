from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Dish, Cook


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = "__all__"
        widgets = {
            "cooks": forms.CheckboxSelectMultiple(),
            "ingredients": forms.CheckboxSelectMultiple(),
        }


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
        )


class CookExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = ["years_of_experience"]


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255, required=False, label="Search dish by name"
    )


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255, required=False, label="Search cook by username"
    )


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255, required=False, label="Search type by name"
    )


class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255, required=False, label="Search ingredient by name"
    )

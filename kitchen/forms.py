from django import forms
from .models import Dish


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = "__all__"
        widgets = {
            "cooks": forms.CheckboxSelectMultiple(),
            "ingredients": forms.CheckboxSelectMultiple(),
        }


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255, required=False, label="Search dish by name"
    )


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255, required=False, label="Search type by name"
    )


class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255, required=False, label="Search ingredient by name"
    )

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cook


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
        )


class CookExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = ["years_of_experience"]


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255, required=False, label="Search cook by username"
    )

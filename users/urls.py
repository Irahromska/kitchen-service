from django.urls import path
from .views import (
    CookListView,
    CookDetailView,
    CookCreateView,
    CookExperienceUpdateView,
    CookDeleteView,
)

app_name = "users"

urlpatterns = [
    path("", CookListView.as_view(), name="cook-list"),
    path("<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("create/", CookCreateView.as_view(), name="cook-create"),
    path("<int:pk>/update/", CookExperienceUpdateView.as_view(), name="cook-update"),
    path("<int:pk>/delete/", CookDeleteView.as_view(), name="cook-delete"),
]

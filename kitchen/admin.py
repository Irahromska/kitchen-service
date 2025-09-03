from django.contrib import admin
from .models import DishType, Dish, Ingredient


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "dish_type", "price")
    list_filter = ("dish_type",)
    search_fields = ("name",)
    filter_horizontal = ("cooks", "ingredients")

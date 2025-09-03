from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return f"{self.username} ({full_name})" if full_name else self.username

    def get_absolute_url(self):
        return reverse("users:cook-detail", kwargs={"pk": self.pk})

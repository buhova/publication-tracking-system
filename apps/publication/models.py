from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def random_badge_class(self):
        colors = [
            "bg-gradient-secondary",
            "bg-gradient-success",
            "bg-gradient-warning",
            "bg-gradient-info",
            "bg-gradient-dark",
        ]
        index = abs(hash(self.name)) % len(colors)
        return colors[index]


class Redactor(AbstractUser):
    years_of_experience = models.PositiveIntegerField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("home:redactor-detail", kwargs={"pk": self.pk})


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="newspapers",
    )
    redactor = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="newspapers"
    )

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title

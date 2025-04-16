from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Topic(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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

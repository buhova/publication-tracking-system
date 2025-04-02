from django.contrib import admin

from publication.models import Topic, Redactor, Newspaper


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Redactor)
class RedactorAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "years_of_experience")
    search_fields = ("first_name", "last_name",)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from publication.models import Topic, Redactor, Newspaper


@admin.register(Redactor)
class RedactorAdmin(admin.ModelAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("years_of_experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "years_of_experience",
                )
            },
        ),
    )
    search_fields = (
        "first_name",
        "last_name",
    )


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "topic",
        "published_date",
    )
    search_fields = ("title",)
    list_filter = ("topic",)


admin.site.register(Topic)

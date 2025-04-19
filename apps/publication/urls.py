from django.urls import path
from .views import (
    index,
    TopicListView,
    RedactorListView,
    RedactorDetailView,
    NewspaperListView,
    NewspaperDetailView,
    NewspaperUpdateView,
    NewspaperCreateView,
    NewspaperDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("redactor/<int:pk>", RedactorDetailView.as_view(), name="redactor-detail"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/<int:pk>", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspapers/create/", NewspaperCreateView.as_view(), name="newspaper-create"),
    path("newspapers/<int:pk>/update/", NewspaperUpdateView.as_view(), name="newspaper-update"),
    path("newspapers/<int:pk>/delete/", NewspaperDeleteView.as_view(), name="newspaper-delete"),
]

app_name = "home"

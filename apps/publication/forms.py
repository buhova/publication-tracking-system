from django import forms
from django.contrib.auth import get_user_model

from .models import Newspaper, Topic


class NewspaperForm(forms.ModelForm):
    redactor = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Newspaper
        fields = ["title", "content", "topic", "redactor"]


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = "__all__"


# Search forms
class RedactorNameSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
    )

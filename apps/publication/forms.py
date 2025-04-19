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

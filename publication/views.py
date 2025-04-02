from django.shortcuts import render

from publication.models import Topic, Redactor, Newspaper


def index(request):
    """View function for the home page of the site."""

    context = {
        "num_topics": Topic.objects.count(),
        "num_newspapers": Newspaper.objects.count(),
        "num_redactors": Redactor.objects.count(),
    }

    return render(request, "publication/index.html", context=context)


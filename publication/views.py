from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from publication.models import Topic, Redactor, Newspaper


def index(request):
    """View function for the home page of the site."""

    context = {
        "num_topics": Topic.objects.count(),
        "num_newspapers": Newspaper.objects.count(),
        "num_redactors": Redactor.objects.count(),
    }

    return render(request, "publication/index.html", context=context)


# class ManufacturerListView(LoginRequiredMixin, generic.ListView):
#     model = Manufacturer
#     context_object_name = "manufacturer_list"
#     template_name = "taxi/manufacturer_list.html"
#     paginate_by = 5

class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "publication/topic_list.html"


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    context_object_name = "redactor_list"
    template_name = "publication/redactor_list.html"


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    context_object_name = "redactor_detail"
    template_name = "publication/redactor_detail.html"


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    context_object_name = "newspaper_list"
    template_name = "publication/newspaper_list.html"


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    context_object_name = "newspaper_detail"
    template_name = "publication/newspaper_detail.html"

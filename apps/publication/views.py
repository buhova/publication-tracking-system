from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from apps.publication.forms import NewspaperForm
from apps.publication.models import Topic, Redactor, Newspaper


def index(request):
    """View function for the home page of the site."""

    context = {
        "num_topics": Topic.objects.count(),
        "num_newspapers": Newspaper.objects.count(),
        "num_redactors": Redactor.objects.count(),
    }

    return render(request, "home/index.html", context=context)


# class ManufacturerListView(LoginRequiredMixin, generic.ListView):
#     model = Manufacturer
#     context_object_name = "manufacturer_list"
#     template_name = "taxi/manufacturer_list.html"
#     paginate_by = 5


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "home/topic_list.html"
    paginate_by = 5


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    form_class = TopicForm
    template_name = "home/topic_form.html"
    success_url = reverse_lazy("home:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = "home/topic_form.html"
    success_url = reverse_lazy("home:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    template_name = "home/topic_confirm_delete.html"
    success_url = reverse_lazy("home:topic-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    context_object_name = "redactor_list"
    template_name = "home/redactor_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        context["search_form"] = RedactorNameSearchForm(initial={"query": query})
        return context

    def get_queryset(self):
        queryset = Redactor.objects.all()
        form = RedactorNameSearchForm(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data.get("query")
            if query:
                queryset = queryset.filter(
                    Q(first_name__icontains=query) | Q(last_name__icontains=query)
                )

        return queryset


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    context_object_name = "redactor_detail"
    template_name = "home/redactor_detail.html"


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    context_object_name = "newspaper_list"
    template_name = "home/newspaper_list.html"
    paginate_by = 5


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper
    context_object_name = "newspaper_detail"
    template_name = "home/newspaper_detail.html"


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "home/newspaper_form.html"
    success_url = reverse_lazy("home:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "home/newspaper_form.html"
    success_url = reverse_lazy("home:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    template_name = "home/newspaper_confirm_delete.html"
    success_url = reverse_lazy("home:newspaper-list")

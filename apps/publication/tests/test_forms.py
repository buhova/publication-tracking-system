from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.publication.forms import NewspaperForm, TopicForm, RedactorNameSearchForm, NewspaperTitleSearchForm
from apps.publication.models import Topic

User = get_user_model()

class NewspaperFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.topic = Topic.objects.create(name="Test Topic")

    def test_newspaper_form_valid_data(self):
        form_data = {
            "title": "Test Title",
            "content": "Test content",
            "topic": self.topic.id,
            "redactor": [self.user.id],
        }
        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_newspaper_form_missing_title(self):
        form_data = {
            "content": "Test content",
            "topic": self.topic.id,
            "redactor": [self.user.id],
        }
        form = NewspaperForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_newspaper_form_redactor_field_queryset(self):
        form = NewspaperForm()
        self.assertIn(self.user, form.fields["redactor"].queryset)

    def test_newspaper_form_redactor_widget(self):
        form = NewspaperForm()
        widget = form.fields["redactor"].widget.__class__.__name__
        self.assertEqual(widget, "CheckboxSelectMultiple")


class TopicFormTest(TestCase):
    def test_topic_form_valid(self):
        form_data = {"name": "New Topic"}
        form = TopicForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_topic_form_missing_name(self):
        form_data = {}
        form = TopicForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class RedactorNameSearchFormTest(TestCase):
    def test_search_form_valid_with_query(self):
        form_data = {"query": "search term"}
        form = RedactorNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_valid_with_empty_query(self):
        form = RedactorNameSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_search_form_label_is_empty(self):
        form = RedactorNameSearchForm()
        self.assertEqual(form["query"].label, "")

    def test_search_form_has_placeholder(self):
        form = RedactorNameSearchForm()
        placeholder = form["query"].field.widget.attrs.get("placeholder", "")
        self.assertEqual(placeholder, "Search")


class NewspaperTitleSearchFormTest(TestCase):
    def test_search_form_valid_with_query(self):
        form_data = {"query": "title"}
        form = NewspaperTitleSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_valid_with_empty_query(self):
        form = NewspaperTitleSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_search_form_label_is_empty(self):
        form = NewspaperTitleSearchForm()
        self.assertEqual(form["query"].label, "")

    def test_search_form_has_placeholder(self):
        form = NewspaperTitleSearchForm()
        placeholder = form["query"].field.widget.attrs.get("placeholder", "")
        self.assertEqual(placeholder, "Search")

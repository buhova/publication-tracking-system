from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.publication.models import Newspaper, Topic

NEWSPAPER_LIST_URL = reverse("home:newspaper-list")


class PublicUserViewTest(TestCase):
    def test_newspaper_login_required(self):
        response = self.client.get(NEWSPAPER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateUserViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            first_name="FirstName",
            last_name="LastName",
            password="my_secret_password",
            years_of_experience=5,
        )
        self.client.force_login(self.user)

        self.topic1 = Topic.objects.create(name="Test Topic 1")
        self.topic2 = Topic.objects.create(name="Test Topic 2")

        self.newspaper1 = Newspaper.objects.create(
            title="Title 1",
            content="Content 1",
            topic=self.topic1
        )
        self.newspaper1.redactor.set([self.user])

        self.newspaper2 = Newspaper.objects.create(
            title="Title 2",
            content="Content 2",
            topic=self.topic2
        )
        self.newspaper2.redactor.set([self.user])

    # Newspaper Tests
    def test_retrieve_newspaper(self):
        response = self.client.get(NEWSPAPER_LIST_URL)
        self.assertEqual(response.status_code, 200)

        newspaper_list = Newspaper.objects.all()
        self.assertEqual(list(response.context["newspaper_list"]),
                         list(newspaper_list))
        self.assertTemplateUsed(response, "home/newspaper_list.html")

    def test_newspaper_search_form_in_context(self):
        response = self.client.get(NEWSPAPER_LIST_URL)
        self.assertIn("search_form", response.context)
        self.assertEqual(response.context["search_form"].initial["query"], "")

    def test_newspaper_search_by_title(self):
        response = self.client.get(NEWSPAPER_LIST_URL, {"query": "Title 1"})
        self.assertContains(response, "Title 1")
        self.assertNotContains(response, "Title 2")

    # NewspaperDetailView
    def test_newspaper_detail_view(self):
        response = self.client.get(
            reverse("home:newspaper-detail", args=[self.newspaper1.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/newspaper_detail.html")
        self.assertEqual(response.context["newspaper_detail"], self.newspaper1)

    # NewspaperCreateView
    def test_newspaper_create_view_get(self):
        response = self.client.get(reverse("home:newspaper-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/newspaper_form.html")
        self.assertIn("topics", response.context)
        self.assertIn("redactors", response.context)

    def test_newspaper_create_view_post(self):
        data = {
            "title": "New Test Title",
            "content": "Some content",
            "topic": self.topic1.id,
            "redactor": [self.user.id]
        }
        response = self.client.post(reverse("home:newspaper-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Newspaper.objects.filter(title="New Test Title").exists())

    # NewspaperUpdateView
    def test_newspaper_update_view_get(self):
        response = self.client.get(
            reverse("home:newspaper-update", args=[self.newspaper1.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/newspaper_form.html")
        self.assertIn("topics", response.context)
        self.assertIn("redactors", response.context)

    def test_newspaper_update_view_post(self):
        response = self.client.post(
            reverse("home:newspaper-update", args=[self.newspaper1.pk]),
            {
                "title": "Updated Title",
                "content": self.newspaper1.content,
                "topic": self.newspaper1.topic.id,
                "redactor": [self.user.id],
            },
        )
        self.newspaper1.refresh_from_db()
        self.assertEqual(self.newspaper1.title, "Updated Title")

    # NewspaperDeleteView Tests
    def test_newspaper_delete_view(self):
        response = self.client.post(
            reverse("home:newspaper-delete", args=[self.newspaper1.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Newspaper.objects.filter(pk=self.newspaper1.pk).exists())

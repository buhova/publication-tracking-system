from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.publication.models import Redactor

REDACTOR_LIST_URL = reverse("home:redactor-list")

class PublicUserViewTest(TestCase):
    def test_redactor_login_required(self):
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)



class PrivateUserRedactorViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            first_name="John",
            last_name="Doe",
            password="password123",
            years_of_experience=3,
        )
        self.client.force_login(self.user)

        self.redactor1 = Redactor.objects.create(
            username="redactor1",
            first_name="Alice",
            last_name="Smith",
            years_of_experience=5,
        )
        self.redactor2 = Redactor.objects.create(
            username="redactor2",
            first_name="Bob",
            last_name="Johnson",
            years_of_experience=2,
        )

    def test_retrieve_redactor_list(self):
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        redactor_list = Redactor.objects.all()
        self.assertEqual(list(response.context["redactor_list"]), list(redactor_list))
        self.assertTemplateUsed(response, "home/redactor_list.html")

    def test_redactor_search_form_in_context(self):
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertIn("search_form", response.context)
        self.assertEqual(response.context["search_form"].initial["query"], "")

    def test_redactor_search_by_first_name(self):
        response = self.client.get(REDACTOR_LIST_URL, {"query": "Alice"})
        self.assertContains(response, "Alice")
        self.assertNotContains(response, "Bob")

    def test_redactor_search_by_last_name(self):
        response = self.client.get(REDACTOR_LIST_URL, {"query": "Johnson"})
        self.assertContains(response, "Johnson")
        self.assertNotContains(response, "Smith")

    def test_redactor_detail_view(self):
        url = reverse("home:redactor-detail", args=[self.redactor1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/redactor_detail.html")
        self.assertEqual(response.context["redactor_detail"], self.redactor1)

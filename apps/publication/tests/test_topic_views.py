from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.publication.models import Newspaper, Topic


TOPIC_LIST_URL = reverse("home:topic-list")


class PublicUserViewTest(TestCase):
    def test_topic_login_required(self):
        response = self.client.get(TOPIC_LIST_URL)
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

    # TopicListView
    def test_retrieve_topic_list(self):
        response = self.client.get(TOPIC_LIST_URL)
        self.assertEqual(response.status_code, 200)

        topic_list = Topic.objects.all()
        self.assertEqual(list(response.context["topic_list"]), list(topic_list))
        self.assertTemplateUsed(response, "home/topic_list.html")

    # TopicCreateView
    def test_topic_create_view_get(self):
        response = self.client.get(reverse("home:topic-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/topic_form.html")

    def test_topic_create_view_post(self):
        data = {"name": "New Created Topic"}
        response = self.client.post(reverse("home:topic-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Topic.objects.filter(name="New Created Topic").exists())

    # TopicUpdateView
    def test_topic_update_view_get(self):
        response = self.client.get(reverse("home:topic-update", args=[self.topic1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/topic_form.html")

    def test_topic_update_view_post(self):
        response = self.client.post(
            reverse("home:topic-update", args=[self.topic1.pk]),
            {"name": "Updated Topic Name"}
        )
        self.assertEqual(response.status_code, 302)
        self.topic1.refresh_from_db()
        self.assertEqual(self.topic1.name, "Updated Topic Name")

    # TopicDeleteView
    def test_topic_delete_view_get(self):
        response = self.client.get(reverse("home:topic-delete", args=[self.topic1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/topic_confirm_delete.html")

    def test_topic_delete_view_post(self):
        response = self.client.post(reverse("home:topic-delete", args=[self.topic1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Topic.objects.filter(pk=self.topic1.pk).exists())

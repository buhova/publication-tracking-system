from django.test import TestCase
from django.urls import reverse

from apps.publication.models import Topic, Redactor, Newspaper


class ModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test")
        self.redactor = Redactor.objects.create_user(
            first_name="FirstName",
            last_name="LastName",
            username="username",
            password="my_secret_password",
            years_of_experience=5,
        )
        self.newspaper = Newspaper.objects.create(
            title="Title",
            content="Content",
            topic=self.topic
        )
        self.newspaper.redactor.set([self.redactor])

    def test_topic_str(self):
        self.assertEqual(str(self.topic), self.topic.name)

    def test_random_badge_class_returns_valid_color(self):
        result = self.topic.random_badge_class
        expected_colors = [
            "bg-gradient-secondary",
            "bg-gradient-success",
            "bg-gradient-warning",
            "bg-gradient-info",
            "bg-gradient-dark",
        ]
        self.assertIn(result, expected_colors)

    def test_redactor_str(self):
        self.assertEqual(str(self.redactor), f"{self.redactor.first_name} {self.redactor.last_name}")

    def test_redactor_password_check(self):
        self.assertTrue(self.redactor.check_password("my_secret_password"))
        self.assertFalse(self.redactor.check_password("wrong_password"))

    def test_redactor_get_absolute_url(self):
        expected_url = reverse("home:redactor-detail", kwargs={"pk": self.redactor.pk})
        self.assertEqual(self.redactor.get_absolute_url(), expected_url)

    def test_newspaper_str(self):
        self.assertEqual(str(self.newspaper), self.newspaper.title)

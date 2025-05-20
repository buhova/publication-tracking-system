from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="my_secret_password"
        )
        self.client.force_login(self.admin_user)

        self.redactor = get_user_model().objects.create_user(
            username="user",
            first_name="FirstName",
            last_name="LastName",
            password="my_secret_password"
        )

    def test_redactor_listed(self):
        """
        Test that redactor's years_of_experience is in list_display on redactor admin page
        :return:
        """
        url = reverse("admin:publication_redactor_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)

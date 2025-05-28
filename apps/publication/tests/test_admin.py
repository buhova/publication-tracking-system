from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from apps.publication.models import Newspaper, Topic


class RedactorAdminTests(TestCase):
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
            password="my_secret_password",
            years_of_experience=5,
        )

    def test_redactor_listed_with_experience(self):
        """
        Test that redactor's years_of_experience is in list_display on redactor admin page
        :return:
        """
        url = reverse("admin:publication_redactor_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_listed_without_experience(self):
        """
        Test that redactor's years_of_experience is not in list_display on redactor admin page
        :return:
        """
        self.redactor.years_of_experience = None
        self.redactor.save()

        url = reverse("admin:publication_redactor_changelist")
        response = self.client.get(url)

        self.assertNotContains(response, "None")

    def test_redactor_detail_with_experience(self):
        """
        Test that redactor's years_of_experience is in list_display on redactor detail admin page
        :return:
        """
        url = reverse("admin:publication_redactor_change", args=[self.redactor.id])
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_detail_shows_years_of_experience_field(self):
        """
        Test that the years_of_experience field is shown in the redactor change form,
        even if its value is None.
        """
        self.redactor.years_of_experience = None
        self.redactor.save()

        url = reverse("admin:publication_redactor_change", args=[self.redactor.id])
        response = self.client.get(url)
        self.assertContains(response, 'name="years_of_experience"')

    def test_redactor_add_form_shows_custom_fields(self):
        """
        Test that the add form for redactor includes first_name, last_name, and years_of_experience
        from the custom add_fieldsets.
        """
        url = reverse("admin:publication_redactor_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="years_of_experience"')

    def test_redactor_admin_search_by_first_and_last_name(self):
        """
        Test that redactor can be found in admin changelist by searching first_name or last_name.
        """
        url = reverse("admin:publication_redactor_changelist")

        # Search by first name
        response = self.client.get(url, {"q": "FirstName"})
        self.assertContains(response, self.redactor.first_name)

        # Search by last name
        response = self.client.get(url, {"q": "LastName"})
        self.assertContains(response, self.redactor.last_name)


class NewspaperAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="my_secret_password"
        )
        self.client.force_login(self.admin_user)

        self.topic = Topic.objects.create(name="Test")
        self.redactor = get_user_model().objects.create_user(
            username="user",
            first_name="FirstName",
            last_name="LastName",
            password="my_secret_password",
            years_of_experience=5,
        )
        self.newspaper = Newspaper.objects.create(
            title="Title",
            content="Content",
            topic=self.topic
        )
        self.newspaper.redactor.set([self.redactor])

    def test_newspaper_listed_with_title_and_topic(self):
        """
        Test that newspaper's title and topic is in list_display on newspaper admin page
        :return:
        """
        url = reverse("admin:publication_newspaper_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.newspaper.title)
        self.assertContains(response, self.newspaper.topic.name)

    def test_newspaper_search_by_title(self):
        """
        Tests searching newspapers by the 'title' field in the Django admin.
        Should return matching newspaper results and exclude non-matching queries.
        """
        url = reverse("admin:publication_newspaper_changelist")

        # Search for an existing newspaper by title
        existing_title = self.newspaper.title
        response = self.client.get(url, {"q": existing_title})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, existing_title)

        # Search for a non-existing newspaper
        non_existing_title = "NonexistentTitle"
        response = self.client.get(url, {"q": non_existing_title})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Newspaper")


    def test_newspaper_list_filter_contains_topic(self):
        """
        Test that the list filter by 'topic' is present
        on the newspaper admin changelist page.
        The filter should show the 'By topic' label
        and include the created topic name.
        """
        url = reverse("admin:publication_newspaper_changelist")
        response = self.client.get(url)

        # Check that the filter label is displayed
        self.assertContains(response, "By topic")
        # Check that the filter includes the topic's name
        self.assertContains(response, self.topic.name)

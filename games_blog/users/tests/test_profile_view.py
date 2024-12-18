from audioop import reverse

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework.reverse import reverse_lazy
from datetime import date
from users.forms import ProfileUpdateForm, UserUpdateForm
from users.models import Profile


class ProfileDetailViewTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ProfileDetailViewTest, cls).setUpClass()
        cls.user = User.objects.create(username="testuser", email="testemail@yahoo.com", password="<PASSWORD>")

        cls.user.profile.birth_date = timezone.now()
        cls.user.profile.bio = "biography data"
        cls.user.profile.save()

        cls.profile_detail_url = reverse_lazy("users:profile_detail", kwargs={"slug": cls.user.profile.slug})

    def test_profile_detail_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(self.profile_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile/profile_detail.html")

    def test_profile_detail_view_anonymous(self):
        response = self.client.get(self.profile_detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users:login") + '?next=' + self.profile_detail_url)


class UserProfileUpdateViewTest(ProfileDetailViewTest):
    @classmethod
    def setUpClass(cls):
        super(UserProfileUpdateViewTest, cls).setUpClass()
        cls.profile_edit_url = reverse_lazy("users:profile_edit", kwargs={"slug": cls.user.profile.slug})
        user_update_form_fields = ("username", "email", "first_name", "last_name")
        cls.user_update_data = {field:getattr(cls.user, field) + "updated" for field in user_update_form_fields }
        cls.profile_update_data = {
            'birth_date': date.today(),
            'bio': 'updated biography data',
        }

    def test_forms(self):
        print(UserUpdateForm(data=self.user_update_data).is_valid())

    def test_profile_update_view_authenticated_valid_data(self):
        self.client.force_login(self.user)

        response = self.client.post(self.profile_edit_url, data={**self.user_update_data, **self.profile_update_data})

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, self.user_update_data['username'])
        self.assertEqual(self.user.email, self.user_update_data['email'])
        self.assertEqual(self.user.first_name, self.user_update_data['first_name'])
        self.assertEqual(self.user.last_name, self.user_update_data['last_name'])
        self.assertEqual(self.user.profile.bio, self.profile_update_data['bio'])
        self.assertEqual(self.user.profile.birth_date, self.profile_update_data['birth_date'])


    def test_profile_update_view_authenticated_invalid_data(self):
        self.client.force_login(self.user)
        response = self.client.post(self.profile_edit_url, {})
        self.assertFormError(response, 'form', 'bio', 'Это поле обязательно для заполнения.')

    def test_profile_update_view_anonymous(self):
        response = self.client.post(self.profile_edit_url, {})
        self.assertRedirects(response, reverse_lazy("users:login") + '?next=' + self.profile_edit_url)
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your tests here.

User = get_user_model()


class UserRegistrationLoginTests(TestCase):
    def test_register_creates_user_and_auto_logins(self):
        url = reverse("users:register")
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password1": "StrongPassw0rd!",
            "password2": "StrongPassw0rd!",
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())
        # After registration, user should be authenticated (auto-login)
        user = resp.context["user"]
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.email, "testuser@example.com")

    def test_login_with_email(self):
        user = User.objects.create_user(email="jane@example.com", password="pass12345", username="jane")
        login_url = reverse("users:login")
        resp = self.client.post(login_url, {"username": "jane@example.com", "password": "pass12345"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["user"].is_authenticated)

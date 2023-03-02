from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.token = Token.objects.create(user=self.user)

    def test_redirect_to_login(self):
        response = self.client.get(reverse('redirect_to_login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login')

    def test_custom_login_view_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/api')

    def test_custom_login_view_valid_form(self):
        response = self.client.post(
            reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/api/overview?token={self.token.key}')

    def test_custom_login_view_invalid_form(self):
        response = self.client.post(
            reverse('login'), {'username': 'testuser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Please enter a correct username and password')

    def test_custom_signup_view_valid_form(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/api/overview?token={self.token.key}')

    def test_custom_signup_view_invalid_form(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'The two password fields didn&#x27;t match.')

    def test_log_out(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('log_out'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login')

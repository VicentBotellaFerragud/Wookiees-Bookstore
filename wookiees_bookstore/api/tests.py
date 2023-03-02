from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Book
from .serializers import BookSerializer
from django.contrib.auth.models import User


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(title='Test Book', author=User.objects.create_user(
            username='test_user', password='test_password'), description='A test book')
        self.book.save()

    def test_redirect_to_api_overview(self):
        response = self.client.get(reverse('redirect_to_api_overview'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, '/api/overview')

    def test_api_overview(self):
        response = self.client.get(reverse('api_overview'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'overview.html')

    def test_book_viewset_get(self):
        client = APIClient()
        response = client.get(reverse('book-list'))
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_book_viewset_post(self):
        client = APIClient()
        user = User.objects.create_user(
            username='test_user', password='test_password')
        client.force_authenticate(user=user)
        data = {'title': 'New Book', 'description': 'A new book'}
        response = client.post(reverse('book-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(
            title='New Book').description, 'A new book')

    def test_book_viewset_post_darth_vader(self):
        client = APIClient()
        user = User.objects.create_user(
            username='Darth_Vader', password='test_password')
        client.force_authenticate(user=user)
        data = {'title': 'New Book', 'description': 'A new book'}
        response = client.post(reverse('book-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_viewset_put(self):
        client = APIClient()
        user = User.objects.create_user(
            username='test_user', password='test_password')
        client.force_authenticate(user=user)
        data = {'title': 'Test Book 2', 'description': 'A test book 2'}
        response = client.put(
            reverse('book-detail', args=[self.book.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(
            id=self.book.id).title, 'Test Book 2')

    def test_book_viewset_delete(self):
        client = APIClient()
        user = User.objects.create_user(
            username='test_user', password='test_password')
        client.force_authenticate(user=user)
        response = client.delete(reverse('book-detail', args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

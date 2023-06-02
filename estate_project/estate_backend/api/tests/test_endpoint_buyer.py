import pytest
import datetime

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from estate_backend.models import Buyer


@pytest.mark.django_db
class TestOwnerViewSetPermissions:
    def test_buyer_view_set_permissions(self, admin_user_client: APIClient):
        # Проверяем доступность endpoint'а для администратора
        response = admin_user_client.get('/api/buyer/')
        assert response.status_code == status.HTTP_200_OK

    def test_buyer_view_set_permissions(self, common_user_client: APIClient):
        # Проверяем доступность endpoint'а для обычного зарегистрированного пользователя
        response = common_user_client.get('/api/buyer/')
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestBuyerViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            password='admin123',
            is_staff=True,
            is_superuser=True,
            date_of_birth=datetime.date(2000, 1, 1),
        )

        cls.custom_user = get_user_model().objects.create_user(
            username='user',
            password='user123',
            date_of_birth=datetime.date(2000, 1, 1)
        )

    def setUp(self):
        self.client = APIClient()

    def test_create_buyer(self):
        self.client.force_authenticate(user=self.admin_user)

        buyer_data = {
            'user': self.admin_user.id,
            'full_name': 'John Doe',
            'phone_number': '+375 (12) 345-67-89',
            'email': 'johndoe@example.com',
        }

        response = self.client.post('/api/buyer/', buyer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        buyer = Buyer.objects.get(id=response.data['id'])
        self.assertEqual(buyer.user, self.admin_user)
        self.assertEqual(buyer.full_name, 'John Doe')
        self.assertEqual(buyer.phone_number, '+375 (12) 345-67-89')
        self.assertEqual(buyer.email, 'johndoe@example.com')

    def test_update_buyer(self):
        self.client.force_authenticate(user=self.admin_user)

        buyer = Buyer.objects.create(
            user=self.admin_user,
            full_name='John Doe',
            phone_number='+375 (12) 345-67-89',
            email='johndoe@example.com',
        )

        buyer_data = {
            'full_name': 'Updated Name',
            'phone_number': '+375 (11) 222-33-44',
            'email': 'updated@example.com',
        }

        response = self.client.patch(f'/api/buyer/{buyer.id}/', buyer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        buyer.refresh_from_db()
        self.assertEqual(buyer.full_name, 'Updated Name')
        self.assertEqual(buyer.phone_number, '+375 (11) 222-33-44')
        self.assertEqual(buyer.email, 'updated@example.com')

    def test_delete_buyer(self):
        self.client.force_authenticate(user=self.admin_user)

        buyer = Buyer.objects.create(
            user=self.admin_user,
            full_name='John Doe',
            phone_number='+375 (12) 345-67-89',
            email='johndoe@example.com',
        )

        response = self.client.delete(f'/api/buyer/{buyer.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Buyer.objects.filter(id=buyer.id).exists())

    def test_get_buyer_detail(self):
        # Test case for retrieving a single buyer detail
        buyer = Buyer.objects.create(
            user=self.admin_user,
            full_name='John Doe',
            phone_number='+375 (12) 345-67-89',
            email='johndoe@example.com',
        )

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/api/buyer/{buyer.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'John Doe')
        self.assertEqual(response.data['phone_number'], '+375 (12) 345-67-89')
        self.assertEqual(response.data['email'], 'johndoe@example.com')

    def test_get_buyer_list(self):
        # Test case for retrieving a list of buyers
        Buyer.objects.create(
            user=self.admin_user,
            full_name='John Doe',
            phone_number='+375 (12) 345-67-89',
            email='johndoe@example.com',
        )
        Buyer.objects.create(
            user=self.custom_user,
            full_name='Jane Smith',
            phone_number='+375 (11) 222-33-44',
            email='janesmith@example.com',
        )

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/buyer/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

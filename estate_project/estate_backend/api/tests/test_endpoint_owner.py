import pytest
from rest_framework import status

from rest_framework.test import APIClient

from estate_backend.models import Owner


@pytest.mark.django_db
class TestOwnerViewSetPermissions:

    def test_owner_view_set_permissions(self, admin_client: APIClient):
        # Проверяем доступность endpoint'а для администратора
        response = admin_client.get('/api/owner/')
        assert response.status_code == status.HTTP_200_OK

    def test_owner_view_set_permissions(self, common_user_client: APIClient):
        # Проверяем доступность endpoint'а для обычного пользователя
        response = common_user_client.get('/api/owner/')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestOwnerViewSet:
    def test_create_owner(self, admin_client, admin_user):
        url = '/api/owner/'
        data = {
            'user': admin_user.id,
            'full_name': 'John Doe',
            'phone_number': '+375 (12) 345-67-89',
            'email': 'johndoe@example.com',
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Owner.objects.filter(**data).exists()

    def test_update_owner(self, admin_client, owner):
        url = f'/api/owner/{owner.pk}/'
        data = {
            'user': owner.user.id,
            'full_name': 'John Updated',
            'phone_number': '+375 (12) 345-67-90',
            'email': 'johnupdated@example.com'
        }
        response = admin_client.put(url, data, format='json', content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        owner.refresh_from_db()
        assert Owner.objects.filter(**data).exists()

    def test_delete_owner(self, admin_client, owner):
        url = f'/api/owner/{owner.pk}/'
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Owner.objects.filter(pk=owner.pk).exists()

    def test_get_owner_detail(self, admin_client, owner):
        url = f'/api/owner/{owner.pk}/'
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['full_name'] == owner.full_name
        assert response.data['phone_number'] == owner.phone_number
        assert response.data['email'] == owner.email

    def test_get_owner_list(self, admin_user_client, owner):
        url = '/api/owner/'
        response = admin_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['full_name'] == owner.full_name
        assert response.data[0]['phone_number'] == owner.phone_number
        assert response.data[0]['email'] == owner.email

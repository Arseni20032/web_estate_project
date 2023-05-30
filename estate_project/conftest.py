import pytest

from estate_backend.models import CustomUser
from rest_framework.test import APIClient


@pytest.fixture(scope='function')
def admin_client(django_db_setup):
    api_client = APIClient()
    user = CustomUser.objects.create_user(
        username='ars',
        email='qwerty@mail.ru',
        password='1234',
        date_of_birth="2000-01-01",
        timezone="UTC"
    )
    api_client.login(user)
    return api_client


@pytest.fixture(scope='function')
def common_user_client(django_db_setup):
    api_client = APIClient()
    user = CustomUser.objects.create_user(
        username='ars',
        is_staff=False,
        is_superuser=False,
        email='qwerty@mail.ru',
        password='1234',
        date_of_birth="2000-01-01",
        timezone="UTC"
    )
    api_client.login(user)
    return api_client
#
# # @pytest.fixture
# # def custom_user_fixture(db):
# #     user = CustomUser.objects.create(username="yourusername", password="yourpassword", email="youremail@example.com", date_of_birth="2000-01-01", timezone="UTC")
# #     return user
#
# # @pytest.fixture(scope='function')
# # def user_client(django_db_setup):
# #     client = Client()
# #     user = User.objects.create_user(
# #         username='test_client',
# #         email='test_user@example.com',
# #         password='password',
# #         is_superuser=False
# #     )
# #     return client
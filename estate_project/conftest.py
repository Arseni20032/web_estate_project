import datetime

import pytest

from estate_backend.models import Buyer, CustomUser, Owner
from rest_framework.test import APIClient
@pytest.fixture
def admin_user() -> CustomUser:
    admin_user = CustomUser.objects.create(
        username='admin',
        is_superuser=True,
        is_staff=True,
        date_of_birth=datetime.date(2000, 1, 1)
    )
    return admin_user


@pytest.fixture
def common_user() -> CustomUser:
    common_user = CustomUser.objects.create(
        username='common_user',
        is_superuser=False,
        is_staff=False,
        date_of_birth=datetime.date(2000, 1, 1)
    )
    return common_user


@pytest.fixture
def admin_user_client(admin_user) -> APIClient:
    api_client = APIClient()
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def common_user_client(common_user) -> APIClient:
    api_client = APIClient()
    api_client.force_authenticate(user=common_user)
    return api_client


@pytest.fixture
def buyer() -> Buyer:
    buyer = Buyer.objects.create(
        user=admin_user.id,
        full_name='John Byuer',
        phone_number='+375 (12) 345-67-89',
        email='johndoe@example.com',
    )
    return buyer


@pytest.fixture
def owner(common_user: CustomUser) -> Owner:
    owner = Owner.objects.create(
        user=common_user,
        full_name='John Owner',
        phone_number='+375 (12) 345-67-89',
        email='johndoe@example.com',
    )
    return owner

import pytest

from estate_backend.models import CustomUser
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_goods_view_details_allowed(common_user_client: APIClient):
    response = common_user_client.get(f'/api/estate/')
    assert response.status_code == 200



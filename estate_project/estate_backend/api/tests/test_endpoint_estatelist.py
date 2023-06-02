import pytest

from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
def test_goods_view_details_allowed(common_user_client: APIClient):
    response = common_user_client.get(f'/api/estate/list/')
    assert response.status_code == status.HTTP_200_OK

import datetime

import pytest

from estate_backend.models import EstateType, Owner, CustomUser


@pytest.mark.django_db
def test_create_estate_type():
    category = EstateType.objects.create(type_estate="dom")
    assert category.type_estate == "dom"


# @pytest.fixture
# def user_fixture(db):
#     return CustomUser.objects.create(
#         first_name="Antoha",
#         last_name="Krytou",
#         email="qwerty@mail.ru",
#         username="ars123",
#         is_staff=True,
#         date_of_birth=datetime.date(2000, 10, 10)
#
#     )

# @pytest.mark.django_db
# def test_create_estate_type():
#     category = Owner.objects.create(full_name="Antoha")
#     assert category.full_name == "Antoha"

@pytest.mark.django_db
def test_owner_creation(admin_client):
    # Создание экземпляра Owner, используя фикстуру custom_user_fixture
    owner = Owner.objects.create(user=admin_client, full_name="John Doe")

    # Проверка корректности создания Owner
    assert owner.user == admin_client
    assert owner.full_name == "John Doe"






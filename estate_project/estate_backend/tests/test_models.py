import pytest
from django.core.exceptions import ValidationError

from estate_backend.models import EstateType, Owner, Buyer


@pytest.mark.django_db
def test_create_estate_type():
    category = EstateType.objects.create(type_estate="dom")
    category.full_clean()
    assert category.type_estate == "dom"


@pytest.mark.django_db
def test_owner_creation(admin_user):
    owner = Owner.objects.create(
        user=admin_user,
        full_name="John Doe",
        email="ololo@gmail.com",
        phone_number="+375 (33) 632-89-63"
    )
    owner.full_clean()
    assert owner.user == admin_user
    assert owner.full_name == "John Doe"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "phone_number",
    [
        '+1234567890',  # Phone number without the required format
        '+375 123456789',  # Phone number without the required format
        '+375 (12) 123-456',  # Phone number without the required format
        '+375 (12) 123-45-6789',  # Phone number with too many digits
        '1234567890',  # Phone number without the required format
        '375 (12) 123-4567',  # Phone number without the required format
        '375 (12) 123-45-6789',
    ]
)
def test_buyer_phone_number_validator(phone_number):
    buyer = Buyer(phone_number=phone_number)
    with pytest.raises(ValidationError):
        buyer.full_clean()

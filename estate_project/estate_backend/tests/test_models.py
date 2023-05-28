from estate_project.estate_backend.models import EstateType


def test_create_estate_type():
    category = EstateType.objects.create(name="dom")
    assert category.name == "dom"

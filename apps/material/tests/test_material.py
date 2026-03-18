import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from kernel.identity.models import User
from apps.material.models import Category, Uom, Item


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    user = User.objects.create_user(username="testuser", password="password")
    return user


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
def test_create_category(auth_client):
    url = reverse('category-list')
    data = {
        "code": "ELEC",
        "name": "Electronics"
    }
    response = auth_client.post(url, data, format='json')
    assert response.status_code == 200
    assert response.data['success'] is True
    assert response.data['data']['code'] == "ELEC"
    assert Category.objects.count() == 1


@pytest.mark.django_db
def test_create_uom(auth_client):
    url = reverse('uom-list')
    data = {
        "code": "PCS",
        "name": "Pieces"
    }
    response = auth_client.post(url, data, format='json')
    assert response.status_code == 200
    assert response.data['success'] is True
    assert response.data['data']['code'] == "PCS"
    assert Uom.objects.count() == 1


@pytest.mark.django_db
def test_create_item(auth_client, user):
    cat = Category.objects.create(code="ELEC", name="Electronics", created_by=user)
    uom = Uom.objects.create(code="PCS", name="Pieces", created_by=user)

    url = reverse('item-list')
    data = {
        "code": "ITEM-001",
        "name": "Laptop",
        "category": cat.id,
        "base_uom": uom.id,
        "status": "DRAFT"
    }
    response = auth_client.post(url, data, format='json')
    assert response.status_code == 200
    assert response.data['success'] is True
    assert response.data['data']['code'] == "ITEM-001"
    assert Item.objects.count() == 1

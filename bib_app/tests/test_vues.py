import pytest
from django.urls import reverse
from django.test import Client
from bib_app.models import Livre
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_livre_detail_view():
    client = Client()
    Livre.objects.create(titre="test",
                         isbn="9780451524935",
                         synopsis="test")
    path = reverse('detail_livre', kwargs={'livre_id': 1})
    response=client.get(path)
    assert response.status_code == 302
    assertTemplateUsed(response, "detail_livre.html")
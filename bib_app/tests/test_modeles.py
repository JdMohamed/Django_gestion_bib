import pytest

from django.test import Client
from bib_app.models import Livre


@pytest.mark.django_db
def test_livre_modele():
    client= Client()
    livre = Livre.objects.create(titre="test",
                         isbn="9780451524935",
                         synopsis="test")
    expected_value = "test"
    assert str(livre) == expected_value


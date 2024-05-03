import pytest
from django.urls import reverse, resolve
from bib_app.models import Livre


@pytest.mark.django_db
def test_livre_detail_url():
    Livre.objects.create(titre="test",
                         isbn="9780451524935",
                         synopsis="test")
    path = reverse('detail_livre', kwargs={'livre_id': 1})
    #path = reverse('infos', kwargs={'pk': 1})

    assert path == "/livres/1/"

    assert resolve(path).view_name == "detail_livre"
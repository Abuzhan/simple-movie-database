import uuid


def test_404(client):
    # given
    url = f'/{str(uuid.uuid4())}'

    # when
    _, response = client.get(url)

    # then
    assert response.status_code == 404

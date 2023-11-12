def test_login_returns_token(client):
    # given
    url = '/v1/login'

    # when
    _, response = client.post(url)

    # then
    assert response.status_code == 200
    assert 'token' in response.json['data']

def test_create_movie_returns_400_when_request_body_is_invalid(client):
    # given
    url = '/v1/movies.create'
    request_body = {}

    # when
    _, response = client.post(url, json=request_body)

    # then
    assert response.status_code == 400


def test_get_all_movies_returns_empty_list_when_no_movies_exist(client):
    # given
    url = '/v1/movies.list'

    # when
    _, response = client.get(url)

    # then
    assert response.status_code == 200
    assert len(response.json['data']) == 0


def test_get_movie_returns_404_when_movie_does_not_exist(client):
    # given
    url = '/v1/movies.get/test'

    # when
    _, response = client.get(url)

    # then
    assert response.status_code == 404


def test_delete_movie_returns_401_when_not_authorized(client):
    # given
    url = '/v1/movies.delete/test'

    # when
    _, response = client.delete(url)

    # then
    assert response.status_code == 401


def test_delete_movie_succeeds_when_authenticated(client):
    # given
    login_url = '/v1/login'
    url = '/v1/movies.delete/test'
    _, login_result = client.post(login_url)
    assert login_result.status_code == 200
    print(login_result)
    token = login_result.json['data']['token']

    # when
    _, response = client.delete(url, headers={'Authorization': f'Bearer {token}'})

    # then
    assert response.status_code == 204

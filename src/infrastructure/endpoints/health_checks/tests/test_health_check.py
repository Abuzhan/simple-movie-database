def test_readiness_route(client):
    # given
    url = '/health-checks/ready'

    # when
    _, response = client.get(url)

    # then
    assert response.status_code == 200


def test_liveness_route(client):
    # given
    url = '/health-checks/live'

    # when
    _, response = client.get(url)

    # then
    assert response.status_code == 200

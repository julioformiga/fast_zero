def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()
    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_error_400_not_user(client, user):
    response = client.post(
        '/token',
        data={'username': '0', 'password': user.clean_password},
    )
    assert response.status_code == 400


def test_get_token_error_400_wrong_password(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': 0},
    )
    assert response.status_code == 400

from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_error_400_username_registred(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Email already registered'}


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_update_user_wrong_user(client, user_other, token):
    response = client.put(
        f'/users/{user_other.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'email': user_other.email,
            'password': user_other.password,
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user_not_enough_permissions(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'email': user.email,
            'password': user.password,
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}


# def test_update_user_404_user_not_found(client, user, token):
#     response = client.put(
#         f'/users/{user.id}',
#         headers={'Authorization': f'Bearer {token}'},
#         json=None,
#     )
#     assert response.status_code == 404
#     assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}


def test_delete_user_user_not_found(client, user_other, token):
    response = client.delete(
        f'/users/{user_other.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}

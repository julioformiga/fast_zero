from jose import jwt

from fast_zero.security import create_access_token
from fast_zero.settings import Settings


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = jwt.decode(token, Settings().SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']  # Testa se o valor de exp foi adicionado ao token

from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.models import User


def test_db_session(session):
    assert session == Session()


def test_create_user(session):
    new_user = User(
        username='alice', password='secret', email='alice@example.com'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'

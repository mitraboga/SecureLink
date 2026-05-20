import pytest

from app.database import Base, engine
from app.models import conversation_session, message, security_event, user  # noqa: F401


@pytest.fixture(autouse=True)
def reset_database() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

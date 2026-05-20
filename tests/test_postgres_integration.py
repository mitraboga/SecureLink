import os

import pytest
from sqlalchemy import create_engine, text


@pytest.mark.skipif(
    not os.getenv("SECURELINK_POSTGRES_TEST_URL"),
    reason="Set SECURELINK_POSTGRES_TEST_URL to run Dockerized PostgreSQL integration test",
)
def test_postgres_connection_for_dockerized_database() -> None:
    engine = create_engine(os.environ["SECURELINK_POSTGRES_TEST_URL"])
    with engine.connect() as connection:
        assert connection.execute(text("select 1")).scalar_one() == 1

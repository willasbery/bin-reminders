import logging

from sqlmodel import Session

from core.db import engine, del_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def delete() -> None:
    with Session(engine) as session:
        del_db(session)


def main() -> None:
    logger.info("Creating initial data")
    delete()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
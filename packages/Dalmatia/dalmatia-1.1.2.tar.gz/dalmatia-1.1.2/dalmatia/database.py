"""This module contains the database functionality."""

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import sqlalchemy as sql
import sqlalchemy.orm as sqlo
from sqlalchemy.orm import Session


class Database:
    """A class that contains database functions."""

    base = sqlo.declarative_base()

    def __init__(self: "Database", path: Path) -> None:
        """Initialize the class.

        Args:
            path: The path to the database file.
        """
        self.__engine__ = sql.create_engine(str(f"sqlite:///{path}"))
        self.base.metadata.create_all(self.__engine__)
        self.__session__ = sqlo.sessionmaker(bind=self.__engine__)

    @contextmanager
    def db_session(self: "Database") -> Iterator[Session]:
        """Context manager for a database session.

        Returns:
            The database session.
        """
        session = self.__session__()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def set_data(
        self: "Database",
        table: sqlo.DeclarativeMeta,
        data: dict[str, None | int | float | str | bytes],
    ) -> None:
        """Update data in the database or add if it does not exist.

        Args:
            table: The table to update the data in.
            data: The data to be updated.
        """
        with self.db_session() as session:
            for key, value in data.items():
                record = session.query(table).filter_by(key=key).first()
                if record is not None:
                    record.value = value
                else:
                    new_record = table(key=key, value=value)
                    session.add(new_record)

    def delete_data(
        self: "Database",
        table: sqlo.DeclarativeMeta,
        key: str,
    ) -> None:
        """Delete data from the database.

        Args:
            table: The table to delete the data from.
            key: The key of the data to be deleted.
        """
        with self.db_session() as session:
            record = session.query(table).filter_by(key=key).first()
            if record is not None:
                session.delete(record)

    def get_data(
        self: "Database",
        table: sqlo.DeclarativeMeta,
        key: str,
    ) -> str:
        """Get data from the database.

        Args:
            table: The table to get the data from.
            key: The key to get the data for.

        Returns:
            The data from the database.
        """
        with self.db_session() as session:
            record = session.query(table).filter_by(key=key).first()
            return record.value if record is not None else "NULL"

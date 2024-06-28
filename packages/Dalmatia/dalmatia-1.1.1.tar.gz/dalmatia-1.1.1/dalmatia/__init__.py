"""This package contains utility functions."""

from dalmatia.database import Database
from dalmatia.forger import Forger
from dalmatia.reader import Reader
from dalmatia.wrapper import Wrapper


class Utils:
    """A class that contains utility functions."""

    (
        database,
        forge,
        reader,
        wrap,
    ) = (
        Database,
        Forger,
        Reader,
        Wrapper,
    )

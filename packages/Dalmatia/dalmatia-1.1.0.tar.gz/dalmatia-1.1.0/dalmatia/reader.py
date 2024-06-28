"""This module contains the Reader class."""

from pathlib import Path


class Reader:
    """A class that contains read functions."""

    @staticmethod
    def file(path: Path) -> str:
        """Read a file.

        Args:
            path: The path to the file.
        """
        try:
            return path.read_text()
        except Exception as e:
            err_msg = f"Failed to read file {path}. Error: {e!s}"
            raise OSError(err_msg) from e

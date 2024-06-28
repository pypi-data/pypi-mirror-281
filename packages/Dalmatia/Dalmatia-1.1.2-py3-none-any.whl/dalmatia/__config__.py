"""This module contains configuration settings."""

from pathlib import Path

from dalmatia import Utils

# General
# =============================================================================
BASE_DIR: Path = Path(__file__).resolve().parent
TESTS_DIR: Path = Utils.forge.dir(BASE_DIR / "tests")
# =============================================================================

# Database
# =============================================================================
TEST_DATABASE_DIR: Path = Utils.forge.dir(TESTS_DIR / "database")
TEST_DATABASE_FILE: Path = Utils.forge.file(
    TEST_DATABASE_DIR / "test_database.db",
)
# =============================================================================

# .so Lib files
# =============================================================================
LIB_DIR: Path = Utils.forge.dir(BASE_DIR / "build")
UTILS_LIB_FILE: Path = LIB_DIR / "test.so"
# =============================================================================

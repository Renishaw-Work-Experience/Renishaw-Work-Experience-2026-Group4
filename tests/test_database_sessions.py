import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from database import database



class SessionDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_db = os.path.join(self.temp_dir.name, "test.db")
        self.original_db_path = database.db_path
        database.db_path = self.temp_db

        with sqlite3.connect(self.temp_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS Accounts (
                    accountID INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    salt TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS Sessions (
                    sessionID TEXT PRIMARY KEY,
                    userID INTEGER NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.execute(
                "INSERT INTO Accounts (accountID, username, password, salt) VALUES (?, ?, ?, ?)",
                (1, "alice", "pw", "salt"),
            )
            conn.commit()

    def tearDown(self):
        database.db_path = self.original_db_path
        self.temp_dir.cleanup()

    def test_add_session_persists_session_id_and_timestamp(self):
        database.addSession(1, "session-123", "2026-07-15 12:34:56")

        with sqlite3.connect(self.temp_db) as conn:
            row = conn.execute(
                "SELECT sessionID, userID, timestamp FROM Sessions WHERE sessionID = ?",
                ("session-123",),
            ).fetchone()

        self.assertEqual(row, ("session-123", 1, "2026-07-15 12:34:56"))


if __name__ == "__main__":
    unittest.main()

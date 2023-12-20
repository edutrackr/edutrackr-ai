import logging
import os
import sqlite3
import uuid
from api.common.utils.json import try_deserialize_from_json, try_serialize_to_json
from api.persistence.base import IObjectStore


logger = logging.getLogger(__name__)

STORE_TABLE = "STORE"
STORE_SCHEMA = """
(
    ID TEXT NOT NULL,
    DATA TEXT NOT NULL
)
"""

class SQLiteObjectStore(IObjectStore):
    """
    SQLite object store (optimized for distributed processing).
    """
    
    file_path: str
    """
    Full path to the file where the database is stored.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._init_db()

    def get_all(self) -> dict:
        result = {}
        connection = None
        try:
            connection = self._create_connection()
            cursor = connection.execute(f"SELECT ID, DATA FROM {STORE_TABLE};")
            for row in cursor.fetchall():
                result[row[0]] = try_deserialize_from_json(row[1])
        except Exception as e:
            logger.error(e)
        finally:
            if connection:
                connection.close()
        return result

    def get_by_id(self, key: str) -> dict | None:
        result = None
        connection = None
        try:
            connection = self._create_connection()
            cursor = connection.execute(f"SELECT DATA FROM {STORE_TABLE} WHERE ID='{key}';")
            row = cursor.fetchone()
            if row is not None:
                result = try_deserialize_from_json(row[0])
        except Exception as e:
            logger.error(e)
        finally:
            if connection:
                connection.close()
        return result

    def add(self, value: dict) -> str | None:
        key = self._generate_key()
        json_value = try_serialize_to_json(value)
        if json_value is None:
            return None
        connection = None
        try:
            connection = self._create_connection()
            connection.execute(f"INSERT INTO {STORE_TABLE} (ID, DATA) VALUES ('{key}', '{json_value}');")
            connection.commit()
        except Exception as e:
            key = None
            logger.error(e)
        finally:
            if connection:
                connection.close()
        return key
        
    def delete(self, key: str) -> None:
        connection = None
        try:
            connection = self._create_connection()
            connection.execute(f"DELETE FROM {STORE_TABLE} WHERE ID='{key}';")
            connection.commit()
        except Exception as e:
            logger.error(e)
        finally:
            if connection:
                connection.close()

    def clear(self) -> None:
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        self._init_db()

    def _create_connection(self) -> sqlite3.Connection:
        """
        Creates a connection to the database.
        """
        return sqlite3.connect(self.file_path)

    def _init_db(self) -> None:
        """
        Initializes the database file if it does not exist. 
        Creates the file and the directory if they do not exist.
        """
        path = os.path.dirname(self.file_path)
        if not os.path.exists(path):
            os.makedirs(path)
        connection = None
        try:
            connection = self._create_connection()
            cursor = connection.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{STORE_TABLE}';")
            if cursor.fetchone() is None:
                logger.info(f"Initializing database at {self.file_path}")
                connection.execute(f"CREATE TABLE {STORE_TABLE} {STORE_SCHEMA};")
                connection.commit()
        except Exception as e:
            logger.error(e)
        finally:
            if connection:
                connection.close()

    def _generate_key(self) -> str:
        return uuid.uuid4().hex

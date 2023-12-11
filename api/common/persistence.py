import json
import threading
import os
import uuid


class IObjectStore:
    """
    Interface for object store.
    """

    def get_all(self) -> dict:
        """
        Returns all data in the store.
        """
        raise NotImplementedError

    def get_by_id(self, key: str) -> dict | None:
        """
        Returns data by key.
        """
        raise NotImplementedError

    def add(self, value: dict) -> str:
        """
        Adds data to the store.
        Returns the key of the added data.
        """
        raise NotImplementedError

    def delete(self, key: str) -> None:
        """
        Deletes data by key.
        """
        raise NotImplementedError

    def clear(self) -> None:
        """
        Clears the store.
        """
        raise NotImplementedError


class LocalObjectStore(IObjectStore):
    """
    Thread-safe object store.
    """
    
    file_path: str
    """
    Full path to the file where the data is stored.
    """

    lock: threading.Lock
    """
    Lock for thread-safe access to the data.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lock = threading.Lock()
        self._init_db()

    def get_all(self) -> dict:
        with self.lock:
            data = self._load_data()
            return data

    def get_by_id(self, key: str) -> dict | None:
         with self.lock:
            data = self._load_data()
            return data.get(key)

    def add(self, value: dict) -> str:
        key = self._generate_key()
        with self.lock:
            data = self._load_data()
            data[key] = value
            self._save_data(data)
        return key

    def delete(self, key: str) -> None:
        with self.lock:
            data = self._load_data()
            if key in data:
                del data[key]
                self._save_data(data)

    def clear(self) -> None:
        with self.lock:
            self._save_data()

    def _init_db(self) -> None:
        """
        Initializes the data file if it does not exist. 
        Creates the file and the directory if they do not exist.
        """
        path = os.path.dirname(self.file_path)
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.exists(self.file_path):
            self._save_data()

    def _load_data(self) -> dict:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                try:
                    return json.load(file)
                except:
                    return {}
        return {}

    def _save_data(self, data: dict = {}) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def _generate_key(self) -> str:
        return uuid.uuid4().hex

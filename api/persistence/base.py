class IObjectStore:
    """
    Interface for object store (all methods are thread-safe).
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

    def add(self, value: dict) -> str | None:
        """
        Adds data to the store.
        Returns the key of the added data.
        If the returned key is None, the data was not added.
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

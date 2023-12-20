from api.common.constants.persistence import PersistenceStrategy
from api.persistence.base import IObjectStore
from api.persistence.simple import SimpleObjectStore
from api.persistence.sqlite import SQLiteObjectStore


def get_object_store(strategy: str, file_path: str) -> IObjectStore:
    """
    Returns an object store by strategy.
    """
    if strategy == PersistenceStrategy.SIMPLE:
        return SimpleObjectStore(file_path)
    elif strategy == PersistenceStrategy.SQLITE:
        return SQLiteObjectStore(file_path)
    else:
        raise Exception(f"Invalid persistence strategy: {strategy}")

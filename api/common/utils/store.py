import shelve


class KVStore:
    def __init__(self, filename: str):
        self.filename = filename

    def get(self, key: str) -> str | None:
        with self as db:
            return db.get(key)
        
    def set(self, key: str, value: str):
        with self as db:
            db[key] = value
        
    def has(self, key: str) -> bool:
        with self as db:
            return key in db
        
    def delete(self, key: str):
        with self as db:
            if key in db:
                del db[key]

    def __enter__(self):
        self.db = shelve.open(self.filename)
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

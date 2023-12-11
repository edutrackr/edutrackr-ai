import os
import unittest

from api.common.utils.store import LocalObjectStore
from config import TestingConfig

class LocalObjectStoreTest(unittest.TestCase):
    
    def setUp(self):
        self.db_file_path = os.path.join(TestingConfig.TEMP_PATH, 'db.json')
        self.db = LocalObjectStore(file_path=self.db_file_path)
    

    def tearDown(self):
        os.remove(self.db_file_path)
        pass


    def test01_init(self):
        self.assertIsNotNone(self.db)
        self.assertEqual(len(self.db.get_all()), 0)


    def test02_add_and_get_by_id(self):
        record_id = self.db.add({'name': 'Alice', 'age': 30})
        record = self.db.get_by_id(record_id)

        self.assertIsNotNone(record)


    def test03_get_all(self):
        self.db.add({'name': 'Alice', 'age': 30})
        self.db.add({'name': 'Bob', 'age': 25})
        self.db.add({'name': 'Charlie', 'age': 35})

        self.assertEqual(len(self.db.get_all()), 3)


    def test04_delete(self):
        # Test adding an item, deleting it, and ensuring it's not present
        test_data = {"name": "Test", "age": 30}
        key = self.db.add(test_data)
        self.db.delete(key)
        self.assertIsNone(self.db.get_by_id(key))


    def test05_clear(self):
        # Test adding an item, clearing the store, and ensuring it's empty
        test_data = {"name": "Test", "age": 30}
        self.db.add(test_data)
        self.db.clear()
        self.assertEqual(len(self.db.get_all()), 0)

class PersistenceStrategy:
    SIMPLE = 'simple' # JSON file (only for local development)
    SQLITE = 'sqlite' # Optimized for distributed processing

class DbExtension:
    JSON = '.json'
    SQLITE = '.db'

DB_EXTENSION_BY_STRATEGY = {
    PersistenceStrategy.SIMPLE: DbExtension.JSON,
    PersistenceStrategy.SQLITE: DbExtension.SQLITE
}

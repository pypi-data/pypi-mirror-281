from sqlalchemy.dialects import registry

# Corrected registry.register call
registry.register(
    "columnar",  # Dialect name used in connection strings
    "columnar.dialect.couchbase_dialect",  # Module path
    "CouchbaseDialect"  # Class name
)

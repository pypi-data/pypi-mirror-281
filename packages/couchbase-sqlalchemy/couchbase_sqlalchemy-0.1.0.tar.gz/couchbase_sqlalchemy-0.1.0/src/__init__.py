# your_package/__init__.py

# Optional: Import and expose the connect function and exceptions
from .dbapi import connect, Error, DatabaseError, OperationalError, IntegrityError

# Optional: Expose the dialect directly to users (usually not necessary)
from .dialect.couchbase_dialect import CouchbaseDialect

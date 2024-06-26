from setuptools import setup, find_packages

setup(
    name='couchbase-sqlalchemy',
    version='0.1.2',
    author='Ayush Tripathi',
    author_email='ayush.tripathi@couchbase.com',
    description='A SQLAlchemy dialect for Couchbase Columnar.',
    packages=find_packages(),
    url='https://github.com/couchbase/couchbase-sqlalchemy',
    install_requires=[
        'sqlalchemy',
        'couchbase',
    ],
    entry_points={
        'sqlalchemy.dialects': [
            'couchbase.columnar = src.dialect.couchbase_dialect:CouchbaseDialect',
        ],
    },
)

from enum import Enum
from typing import Protocol, Dict, Any

from pydantic import BaseModel, Field

from config import settings


class RelationalDatabase(Protocol):
    """This class is a protocol for all relational databases."""

    def connect(self) -> None:
        ...

    def query(self, query: str) -> None:
        ...


class RelationalDatabaseType(str, Enum):
    """This class is an enum for all relational databases."""

    MYSQL = 'mysql'
    POSTGRES = 'postgres'
    SQLITE = 'sqlite'
    BIGQUERY = 'bigquery'


class RelationalDatabaseConfiguration(BaseModel):
    """This class is a model for all relational database configurations."""
    kind: RelationalDatabaseType
    labels: Dict[str, Any] = Field(default_factory=dict)


class PostgresSQLPoolConfiguration(BaseModel):
    """This class is a model for PostgresSQL pool configuration."""
    pool_size: int = 5


class PostgresSQLConfiguration(RelationalDatabaseConfiguration):
    """This class is a configuration for PostgreSQL."""
    user: str
    password: str
    host: str
    port: int
    database: str

    pool_configuration: PostgresSQLPoolConfiguration = PostgresSQLPoolConfiguration()


class PostgresSQL:
    """This class is a postgres database."""

    def __init__(self, configuration):
        self.configuration = PostgresSQLConfiguration(kind=configuration.kind, **configuration.configuration)

    def connect(self) -> None:
        print(f'Connecting to PostgresSQL on {self.configuration.host}:{self.configuration.port}')
        if (pool_size := self.configuration.pool_configuration.pool_size) < 5:
            print(f"Pool size default value has been changed: {pool_size}")

    def query(self, query: str) -> None:
        print(f'Executing query: {query}')


class GoogleCloudPlatformClientConfiguration(BaseModel):
    """This class is a configuration for Google Cloud Platform."""
    project_id: str


class BigQueryConfiguration(GoogleCloudPlatformClientConfiguration):
    """This class is a configuration for BigQuery."""
    dataset_id: str
    table_id: str


class BigQuery(RelationalDatabase):
    """This class is a bigquery database."""

    def __init__(self, configuration):
        self.configuration = BigQueryConfiguration(kind=configuration.kind, **configuration.configuration)

    def connect(self) -> None:
        print(
            f'Connecting to BigQuery on '
            f'{self.configuration.project_id}:{self.configuration.dataset_id}:{self.configuration.table_id}')

    def query(self, query: str) -> None:
        print(f'Executing query: {query}')


class RelationalDatabaseFactory:
    """This class is a factory for relational databases."""
    DATABASE_CONSTRUCTORS = {
        RelationalDatabaseType.POSTGRES: PostgresSQL,
        RelationalDatabaseType.BIGQUERY: BigQuery
    }

    @classmethod
    def get_database_instance_from_identifier(cls, identifier: str) -> RelationalDatabase:
        """This method returns a relational database instance from an identifier."""
        database_settings = settings.relational[identifier]
        if not (constructor := cls.DATABASE_CONSTRUCTORS.get(database_settings.kind)):
            raise NotImplementedError(f"missing implementation for [{database_settings.kind}] database.")
        return constructor(database_settings)

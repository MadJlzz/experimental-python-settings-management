from database import RelationalDatabaseFactory


def app():
    db = RelationalDatabaseFactory.get_database_instance_from_identifier(identifier="prices")
    db.connect()

    db2 = RelationalDatabaseFactory.get_database_instance_from_identifier(identifier="file-manager")
    db2.connect()


if __name__ == '__main__':
    app()

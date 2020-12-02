"""DBManagerTestFixture for the habit server."""
from habit_server.__init__ import app, db
from habit_server.db_manager import DBManager


class DBManagerTestFixture():
    """Database manager test fixture."""

    def __enter__(self):
        """Initialize test app, db manager, db session.

        :return DMManager: initialized database manager.
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()
            return DBManager(db.session)

    def __exit__(self, exception_type, exception_value, traceback):
        """Clean up database session.

        :param exception_type: unused
        :param exception_value: unused
        :param traceback: unused
        """
        db.session.remove()
        db.drop_all()

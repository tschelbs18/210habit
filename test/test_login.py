"""Test login API functionality."""
from flask import request, url_for
from test.DBManagerTestFixture import DBManagerTestFixture
from app import app


def test_redirect_if_not_logged_in():
    """Redirect to /login if not logged in adn trying to access other pages"""
    with DBManagerTestFixture():
        with app.test_client() as c:
            c.get(
                '/habits',
                content_type='application/x-www-form-urlencoded',
                follow_redirects=True,
            )

            assert request.path == url_for('render_login')

            c.get(
                '/progress',
                content_type='application/x-www-form-urlencoded',
                follow_redirects=True,
            )

            assert request.path == url_for('render_login')

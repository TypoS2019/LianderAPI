from unittest import TestCase

from app.routers.overige.overige_repository import Database_exception


class TestOverigeRepository(TestCase):

    def setUp(self):
        self.database_exception = Database_exception()

    """ Deze file test overige repository en dan specifiek de klasse Database_exception"""
    def test_return_exception_message_based_on_err_should_return_404(self):
        result = self.database_exception.return_exception_message_based_on_err("fakeerror")
        assert result.status_code == 404

    def test_return_exception_message_based_on_err_should_return_500(self):
        result = self.database_exception.return_exception_message_based_on_err("truncated")
        assert result.status_code == 500

    def test_return_exception_message_based_on_err_should_return_503(self):
        result = self.database_exception.return_exception_message_based_on_err("denied")
        assert result.status_code == 503

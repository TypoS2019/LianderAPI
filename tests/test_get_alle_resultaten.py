from unittest import TestCase, mock

from starlette.testclient import TestClient

from app.routers.overige.overige_controller import OverigeController
from app.routers.overige.overige_view import app


class TestGetAlleResultaten(TestCase):
    def setUp(self):
        self.sut = TestClient(app)

    """Deze test controlleerd of get_alle_resultaten de methode collecteer_resultaten van OverigeController aanroept"""
    @mock.patch.object(OverigeController, 'collecteer_resultaten', return_value=[])
    def test_get_alle_resultaten_calls_controller_collecteer_resultaten(self, mock_collecteer_resultaten):
        # Arrange

        # Act
        response = self.sut.get("/opslaan/resultaat?project_id=1&token=1234-1234-1234-1234")

        # Assert
        mock_collecteer_resultaten.assert_called_with('1', 5, 1, 100, False)

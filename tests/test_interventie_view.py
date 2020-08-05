import json
from unittest import TestCase

import mock

from app.routers.overige.overige_authentication_service import AuthenticationService
from app.routers.interventie.interventie_view import app
from app.routers.interventie.interventie_controller import InterventieController
from starlette.testclient import TestClient
from app.routers.interventie.interventie_models import InterventieResponseModel


class TestInterventieView(TestCase):
    """Test_get_interventies test of get_interventies de correcte statuscode (200) teruggeeft"""
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(InterventieController, 'get_interventies', return_value=[])
    def test_get_interventies(self, mock_get_interventie, mocked_auth):
        client = TestClient(app)
        response = client.get("/?project_id=1&token=1234-1234-1234")
        assert response.status_code == 200

    """test_get_interventies_returns_json checkt of het returntype een List is"""
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(InterventieController, 'get_interventies', return_value=[])
    def test_get_interventies_returns_json(self, mock_get_bodies, mocked_auth):
        # arrange
        client = TestClient(app)

        # act
        response = client.get("/?project_id=1&token=1234-1234-1234")

        # assert
        assert response.json() == []

    """test_get_interventies_calls_right_method test of de juiste methode in de controller aangeroepen wordt"""
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(InterventieController, 'get_interventies', return_value=[])
    def test_get_interventies_calls_right_method(self, mock_get_bodies, mocked_auth):
        client = TestClient(app)

        response = client.get("/?project_id=1&token=1234-1234-1234")

        mock_get_bodies.assert_called_with('1')

    """test_delete_interventies test of de delete functie de goede statuscode teruggeeft"""
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(InterventieController, 'delete_interventie', return_value=[])
    def test_delete_interventies(self, mock_delete_interventie, mocked_auth):
        # arrange
        client = TestClient(app)

        response = client.delete("/1?project_id=1&token=1234-1234-1234")

        assert response.status_code == 200

    # Testen of test_post_interventie_return_view een Json terug geeft
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(InterventieController, 'create_interventie', return_value=[])
    @mock.patch.object(InterventieController, 'get_interventies', return_value=[])
    def test_post_interventie_return_view(self, mock_create_interventie, mock_get_interventies, mocked_auth):
        client = TestClient(app)
        response = client.post("/?project_id=1&token=1234-1234-1234", json={
            "json": "1"
        })
        assert response.json() == []

    # Testen of test_post_interventie_status_code_view de juiste status code 200 terug komt
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(InterventieController, 'create_interventie', return_value=[])
    @mock.patch.object(InterventieController, 'get_interventies', return_value=[])
    def test_post_interventie_status_code_view(self, mock_create_interventie, get_get_interventies, mocked_auth):
        client = TestClient(app)
        response = client.post("/?project_id=1&token=1234-1234-1234", json={
            "json": "1",
        })
        assert response.status_code == 201

    # Testen of test_post_interventie_methode_call_view de juiste methode aangeroepen is
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(InterventieController, 'create_interventie', return_value=[])
    @mock.patch.object(InterventieController, 'get_interventies', return_value=[])
    def test_post_interventie_methode_call_view(self, mock_get_interventies, mock_create_interventie, mocked_auth):
        client = TestClient(app)
        response = client.post("/?project_id=1&token=1234-1234-1234", json={
            "json": "1",
        })
        mock_create_interventie.assert_called_with(InterventieResponseModel(), 1)

    # Testen of test_put_interventie_status_code_view de juiste status code terug komt
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(InterventieController, 'update_interventie', return_value=[])
    @mock.patch.object(InterventieController, 'get_interventies', return_value=[])
    def test_put_interventie_status_code_view(self, mock_update_interventie, mock_get_interventies, mocked_auth):
        client = TestClient(app)
        response = client.put("/?project_id=1&token=1234-1234-1234", json={
            "json": "1",
        })
        assert response.status_code == 200

    # Testen of test_put_interventie_return_view Json teruggeeft
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(InterventieController, 'update_interventie', return_value=[])
    @mock.patch.object(InterventieController, 'get_interventies', return_value=[])
    def test_put_interventie_return_view(self, mock_update_interventie, mock_get_interventies, mocked_auth):
        client = TestClient(app)
        response = client.put("/?project_id=1&token=1234-1234-1234", json={
            "json": "1",
        })
        assert response.json() == []

    # Testen of test_put_interventie_methode_call_view de juiste methode aannroept
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(InterventieController, 'update_interventie', return_value=[])
    @mock.patch.object(InterventieController, 'get_interventies', return_value=[])
    def test_put_interventie_methode_call_view(self, mock_get_interventies, mock_update_interventie, mocked_auth):
        client = TestClient(app)
        response = client.put("/?project_id=1&token=1234-1234-1234", json={
            "json": "1",
        })
        mock_update_interventie.assert_called_with(InterventieResponseModel(), 1)

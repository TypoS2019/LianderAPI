from unittest import TestCase

import mock
from starlette.testclient import TestClient

from app.routers.gebeurtenis.gebeurtenis_models import GebeurtenisResponseModel
from app.routers.gebeurtenis.gebeurtenis_controller import GebeurtenisController
from app.routers.gebeurtenis.gebeurtenis_view import app
from app.routers.overige.overige_authentication_service import AuthenticationService


class TestGebeurtenisView(TestCase):
    """test_get_gebeurtenissen test of get_gebeurtenissen de correcte status code teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'get_gebeurtenissen', return_value=[])
    def test_get_gebeurtenissen(self, mock_get_gebeurtenissen, mocked_auth):
        client = TestClient(app)
        response = client.get("/?project_id=1&token=1234-1234-1234")
        assert response.status_code == 200

    """test_get_gebeurtenissen_json test of get_gebeurtenissen de correcte response geeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'get_gebeurtenissen', return_value=[])
    def test_get_gebeurtenissen_json(self, mock_get_gebeurtenissen, mocked_auth):
        client = TestClient(app)
        response = client.get("/?project_id=1&token=1234-1234-1234")
        assert response.json() == []

    """test_get_gebeurtenissen_json_calls_correct_method test of get_gebeurtenissen de correcte methode aanroept"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'get_gebeurtenissen', return_value=[])
    def test_get_gebeurtenissen_json_calls_correct_method(self, mock_get_gebeurtenissen, mocked_auth):
        client = TestClient(app)
        response = client.get("/?project_id=1&token=1234-1234-1234")
        mock_get_gebeurtenissen.assert_called_with('1')

    """test_delete_gebeurtenissen test of delete_gebeurtenis de correcte status code teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'delete_gebeurtenis', return_value=[])
    def test_delete_gebeurtenissen(self, mock_delete_gebeurtenis, mocked_auth):
        client = TestClient(app)
        response = client.delete("/1?project_id=1&token=1234-1234-1234")
        assert response.status_code == 200

    """test_delete_gebeurtenissen_json test of delete_gebeurtenis de correcte response geeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'delete_gebeurtenis', return_value=[])
    def test_delete_gebeurtenissen_json(self, mock_delete_gebeurtenis, mocked_auth):
        client = TestClient(app)
        response = client.delete("/1?project_id=1&token=1234-1234-1234")
        assert response.json() == []

    """test_delete_gebeurtenissen_json_calls_correct_method test of delete_gebeurtenis de correcte methode aanroept"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'delete_gebeurtenis', return_value=[])
    def test_delete_gebeurtenissen_json_calls_correct_method(self, mock_delete_gebeurtenis, mocked_auth):
        client = TestClient(app)
        response = client.delete("/1?project_id=1&token=1234-1234-1234")
        mock_delete_gebeurtenis.assert_called_with(1, 1)

    """test_put_gebeurtenissen test of update_gebeurtenis de correcte status code teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'update_gebeurtenis', return_value=[])
    def test_put_gebeurtenissen(self, mock_put_gebeurtenissen, mocked_auth):
        client = TestClient(app)
        response = client.put("/?project_id=1&token=1234-1234-1234", json={
            "json": "1",
        })
        assert response.status_code == 200

    """test_put_gebeurtenissen_json test of update_gebeurtenis de correcte response geeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'update_gebeurtenis', return_value=[])
    def test_put_gebeurtenissen_json(self, mock_put_gebeurtenissen, mocked_auth):
        client = TestClient(app)
        response = client.put("/?project_id=1&token=1234-1234-1234", json={
            "json": "1",
        })
        assert response.json() == []

    """test_put_gebeurtenissen_calls_correct_method test of update_gebeurtenis de correcte methode aanroept"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'update_gebeurtenis', return_value=[])
    def test_put_gebeurtenissen_calls_correct_method(self, mock_put_gebeurtenissen, mocked_auth):
        client = TestClient(app)
        response = client.put("/?project_id=1&token=1234-1234-1234", json={
            "json": "1",
        })
        mock_put_gebeurtenissen.assert_called_with(GebeurtenisResponseModel(), 1)

    """test_post_gebeurtenissen test of post_gebeurtenis de correcte status code teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'post_gebeurtenis', return_value=[])
    def test_post_gebeurtenissen(self, mock_post_gebeurtenis, mocked_auth):
        client = TestClient(app)
        response = client.post("/?project_id=1&token=1234-1234-1234", json={
            "json": "1",
        })
        assert response.status_code == 201

    """test_post_gebeurtenissen_json test of post_gebeurtenis de correcte response geeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'post_gebeurtenis', return_value=[])
    def test_post_gebeurtenissen_json(self, mock_post_gebeurtenis, mocked_auth):
        client = TestClient(app)
        response = client.post("/?project_id=1&token=1234-1234-1234", json={
            "json": "1",
        })
        assert response.json() == []

    """test_post_gebeurtenissen_calls_correct_method test of post_gebeurtenis de correcte methode aanroept"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'post_gebeurtenis', return_value=[])
    def test_post_gebeurtenissen_calls_correct_method(self, mock_post_gebeurtenis, mocked_auth):
        client = TestClient(app)
        response = client.post("/?project_id=1&token=1234-1234-1234", json={
            "json": "1",
        })
        mock_post_gebeurtenis.assert_called_with(GebeurtenisResponseModel(), 1)

    """testen of juiste methode wordt gebruikt"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'add_interventie_to_gebeurtenis', return_value=[])
    def test_add_interventie_to_gebeurtenis(self, mock_add_interventie, mocked_auth):
        client = TestClient(app)
        gebeurtenis_id = 1
        interventie_id = 2
        project_id = 1
        response = client.post("/1/add_interventie?interventie_id=2&project_id=1&token=1234-1234-1234")
        mock_add_interventie.assert_called_with(gebeurtenis_id, interventie_id, project_id)

    """testen of juiste methode wordt gebruikt"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'remove_interventie_from_gebeurtenis', return_value=[])
    def test_remove_interventie_from_gebeurtenis(self, mock_remove_interventie, mocked_auth):
        client = TestClient(app)
        gebeurtenis_id = 1
        interventie_id = 2
        project_id = 1
        response = client.delete("/1/remove_interventie?interventie_id=2&project_id=1&token=1234-1234-1234")
        mock_remove_interventie.assert_called_with(gebeurtenis_id, interventie_id,  project_id)

    """testen of juiste methode wordt gebruikt"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebeurtenisController, 'update_interventie_in_gebeurtenis', return_value=[])
    def test_update_interventie_in_gebeurtenis(self, mock_update_interventie, mocked_auth):
        client = TestClient(app)
        gebeurtenis_id = 1
        interventie_id = 2
        project_id = 1
        waarde = 3
        response = client.put("/1/update_interventie?interventie_id=2&waarde=3&project_id=1&token=1234-1234-1234")
        mock_update_interventie.assert_called_with(gebeurtenis_id, interventie_id, waarde, project_id)

from unittest import TestCase

import mock
from starlette.testclient import TestClient
import mysql.connector

from app.routers.overige.overige_authentication_service import AuthenticationService
from app.routers.overige.overige_repository import DataMapper
from app.routers.project.project_models import ProjectResponseModel
from app.routers.project.project_view import app
from app.routers.project.project_controller import ProjectController


class TestProjectView(TestCase):
    """test_get_projecten test of get_projecten de correcte status code teruggeeft"""

    def setUp(self):
        self.project_controller = ProjectController()
        self.test_model = ProjectResponseModel()
        self.test_token = "1234-1234-1234-1234"
        self.test_id = 1

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'get_alle_projecten', return_value=[ProjectResponseModel()])
    def test_get_projecten(self, mock_get_alle_projecten, mocked_auth):
        client = TestClient(app)
        response = client.get("/?token=" + self.test_token)
        assert response.status_code == 200

    """test_get_projecten_json test of get_projecten een json lijst teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'get_alle_projecten', return_value=[ProjectResponseModel()])
    def test_get_project_json(self, mock_get_alle_projecten, mocked_auth):
        client = TestClient(app)
        response = client.get("/?token=" + self.test_token)
        assert response.json() == [{'datum': '2019-12-16', 'id': 1, 'naam': 'projectnaam'}]

    """test_get_project_calls_correct_method test of de correcte methode in de controller wordt aangeroepen"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'get_alle_projecten', return_value=[])
    def test_get_project_calls_correct_method(self, mock_get_alle_projecten, mocked_auth):
        client = TestClient(app)
        client.get("/?token=" + self.test_token)
        mock_get_alle_projecten.assert_called_with('admin')

    """test_get_project_by_id test of get_projecten de correcte status code teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'get_project_by_id', return_value=ProjectResponseModel())
    def test_get_project_by_id(self, mock_get_project_by_id, mocked_auth):
        client = TestClient(app)
        response = client.get("/1?token=test")
        assert response.status_code == 200

    """test_get_project_by_id_json test of get_projecten een json object teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'get_project_by_id', return_value=ProjectResponseModel())
    def test_get_project_by_id_json(self, mock_get_project_by_id, mocked_auth):
        client = TestClient(app)
        response = client.get("/1?token=test")
        assert response.json() == {'datum': '2019-12-16', 'id': 1, 'naam': 'projectnaam'}
        # deze regel moet aangepast worden wanneer er echte models worden toegevoegd

    """test_get_project_by_id_calls_correct_method test of de correcte methode in de controller wordt aangeroepen"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'get_project_by_id', return_value=[])
    def test_get_project_by_id_calls_correct_method(self, mock_get_project_by_id, mocked_auth):
        client = TestClient(app)
        client.get("/" + str(self.test_id) + "?token=" + self.test_token)
        mock_get_project_by_id.assert_called_with(self.test_id, self.test_token)

    """test_post_project test of post_project de correcte status code teruggeeft"""

    @mock.patch.object(DataMapper, '_data_handler', return_value=[])
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'create_project', return_value=[])
    def test_post_project(self, mock_create_project, mocked_auth, mocked_db):
        client = TestClient(app)
        response = client.post("/?token=" + self.test_token, json={
            "id": "1",
        })
        assert response.status_code == 201

    """test_post_project_json test of post_project een json lijst teruggeeft"""

    @mock.patch.object(DataMapper, '_data_handler', return_value=[])
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'create_project', return_value=[])
    def test_post_project_json(self, mock_create_project, mocked_auth, mocked_db):
        client = TestClient(app)
        response = client.post("/?token=" + self.test_token, json={
            "id": "1",
        })
        assert response.json() == []

    """test_post_project_calls_correct_method test of de correcte methode in de controller wordt aangeroepen"""

    @mock.patch.object(DataMapper, '_data_handler', return_value=[])
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'create_project', return_value=[])
    def test_post_project_calls_correct_method(self, mock_create_project, mocked_auth, mocked_db):
        client = TestClient(app)
        client.post("/?token=" + self.test_token, json={
            "id": "1",
        })
        mock_create_project.assert_called_with(self.test_model,
                                               None)  # None omdat de test-token Admin geen user ID heeft

    """test_update_project test of update_project de correcte status code teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'update_project', return_value=[])
    def test_update_project(self, mock_update_project, mocked_auth):
        client = TestClient(app)
        response = client.put("/?token=test", json={
            "id": "1",
        })
        assert response.status_code == 200

    """test_update_project tes of update_project een json lijst teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'update_project', return_value=[])
    def test_update_project_json(self, mock_update_project, mocked_auth):
        client = TestClient(app)
        response = client.put("/?token=test", json={
            "id": "1",
        })
        assert response.json() == []

    """test_update_project_calls_correct_method test of de correcte methode in de controller wordt aangeroepen"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'update_project', return_value=[])
    def test_update_project_calls_correct_method(self, mock_update_project, mocked_auth):
        client = TestClient(app)
        client.put("/?token=" + self.test_token, json={
            "id": str(self.test_id),
        })
        mock_update_project.assert_called_with(self.test_model, self.test_token)

    """test_delete_project test of delete_project de juiste status code teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'delete_project', return_value=[])
    def test_delete_project(self, mock_delete_project, mocked_auth):
        client = TestClient(app)
        response = client.delete("/1?token=test")
        assert response.status_code == 200

    """test_delete_project_json test of delete_project een json lijst teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'delete_project', return_value=[])
    def test_delete_project_json(self, mock_delete_project, mocked_auth):
        client = TestClient(app)
        response = client.delete("/1?token=test")
        assert response.json() == []

    """test_delete_project_calls_correct_method test of de correcte methode in de controller wordt aangeroepen"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'delete_project', return_value=[])
    def test_delete_project_calls_correct_method(self, mock_delete_project, mocked_auth):
        client = TestClient(app)
        client.delete("/" + str(self.test_id) + "?token=" + self.test_token)
        mock_delete_project.assert_called_with(self.test_id, self.test_token)

    """test_voeg_gebruiker_toe_aan_project test of voeg_gebruiker_toe_aan_project de juiste status code teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'voeg_gebruiker_toe_aan_project', return_value=[])
    def test_voeg_gebruiker_toe_aan_project(self, mock_voeg_gebruiker_toe_aan_project, mocked_auth):
        client = TestClient(app)
        response = client.post("/1/1?token=test")
        assert response.status_code == 201

    """test_voeg_gebruiker_toe_aan_project_json test of voeg_gebruiker_toe_aan_project_json een json lijst teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'voeg_gebruiker_toe_aan_project', return_value=[])
    def test_voeg_gebruiker_toe_aan_project_json(self, mock_voeg_gebruiker_toe_aan_project, mocked_auth):
        client = TestClient(app)
        response = client.post("/1/1?token=test")
        assert response.json() == []

    """test_voeg_gebruiker_toe_aan_project_calls_correct_method test of de correcte methode in de controller wordt 
    aangeroepen """

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'voeg_gebruiker_toe_aan_project', return_value=[])
    def test_voeg_gebruiker_toe_aan_project_calls_correct_method(self, mock_voeg_gebruiker_toe_aan_project,
                                                                 mocked_auth):
        client = TestClient(app)
        client.post("/" + str(self.test_id) + "/" + str(self.test_id) + "?token=" + self.test_token)
        mock_voeg_gebruiker_toe_aan_project.assert_called_with(self.test_id, self.test_id, self.test_token)

    """test_verwijder_gebruiker_uit_project test of verwijder_gebruiker_uit_project de juiste status code teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'verwijder_gebruiker_uit_project', return_value=[])
    def test_verwijder_gebruiker_uit_project(self, mock_verwijder_gebruiker_uit_project, mocked_auth):
        client = TestClient(app)
        response = client.delete("/1/1?token=test")
        assert response.status_code == 200

    """test_verwijder_gebruiker_uit_project_json test of verwijder_gebruiker_uit_project_json een json lijst 
    teruggeeft """

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'verwijder_gebruiker_uit_project', return_value=[])
    def test_verwijder_gebruiker_uit_project_json(self, mock_verwijder_gebruiker_uit_project, mocked_auth):
        client = TestClient(app)
        response = client.delete("/1/1?token=test")
        assert response.json() == []

    """test_verwijder_gebruiker_uit_project_calls_correct_method test of de correcte methode in de controller wordt 
    aangeroepen """

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(ProjectController, 'verwijder_gebruiker_uit_project', return_value=[])
    def test_verwijder_gebruiker_uit_project_calls_correct_method(self, mock_verwijder_gebruiker_uit_project,
                                                                  mocked_auth):
        client = TestClient(app)
        client.delete("/" + str(self.test_id) + "/" + str(self.test_id) + "?token=" + self.test_token)
        mock_verwijder_gebruiker_uit_project.assert_called_with(self.test_id, self.test_id, self.test_token)

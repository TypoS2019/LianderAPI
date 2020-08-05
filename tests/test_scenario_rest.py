from unittest import TestCase, mock

from fastapi import HTTPException
from starlette.testclient import TestClient

from app.routers.overige.overige_authentication_service import AuthenticationService
from app.routers.scenario.scenario_controller import ScenarioController
from app.routers.scenario.scenario_models import ScenarioResponseModel
from app.routers.scenario.scenario_view import app


class TestGetScenario(TestCase):
    """ Testen van GET uit de view(scenario) op status code 200"""

    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[])
    def test_get_scenario(self, mock_get_all_scenarios):
        client = TestClient(app)
        response = client.get("/?project_id=1&token=1234-1234-1234-1234")
        assert response.status_code == 200

    """Testen van GET uit de view(scenario) op json return"""

    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[])
    def test_get_scenario_json(self, mock_get_all_scenarios):
        client = TestClient(app)
        response = client.get("/?project_id=1&token=1234-1234-1234-1234")
        assert response.json() == []

    """Testen van GET uit de view(scenario) op aanroep juiste methode"""

    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[])
    def test_get_scenario_json_calls_correct_method(self, mock_get_all_scenarios):
        client = TestClient(app)
        response = client.get("/?project_id=1&token=1234-1234-1234-1234")
        mock_get_all_scenarios.assert_called_with('1')

    """Testen van GET uit de view(scenario) op status code 200"""

    @mock.patch.object(ScenarioController, 'delete_scenario', return_value=None)
    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[])
    def test_delete_scenario(self, mock_delete_scenario, mock_get_all_scenarios):
        client = TestClient(app)
        response = client.delete("/1?project_id=1&token=1234-1234-1234-1234")
        assert response.status_code == 200

    """Testen van DELETE uit de view(scenario) op json return"""

    @mock.patch.object(ScenarioController, 'delete_scenario', return_value=[])
    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[])
    def test_delete_scenario_json(self, mock_delete_scenario, mock_get_all_scenarios):
        client = TestClient(app)
        response = client.delete("/1?project_id=1&token=1234-1234-1234-1234")
        assert response.json() == []

    """Testen van DELETE uit de view(scenario) op aanroep juiste methode"""

    @mock.patch.object(ScenarioController, 'delete_scenario', return_value=[])
    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[])
    def test_delete_scenario_json_calls_correct_method(self, mock_delete_scenario, mock_get_all_scenarios):
        client = TestClient(app)
        response = client.delete("/1?project_id=1&token=1234-1234-1234-1234")
        mock_delete_scenario.assert_called_with(1)

    """Testen van PUT uit de view(scenario) op status code 200"""

    @mock.patch.object(ScenarioController, 'update_scenario', return_value=[])
    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[])
    def test_put_scenario(self, mock_put_scenario, mock_get_all_scenarios):
        client = TestClient(app)
        response = client.put("/?project_id=1&token=1234-1234-1234-1234", json={
            "json": "1",
        })
        assert response.status_code == 200

    """Testen van PUT uit de view(scenario) op json return"""

    @mock.patch.object(ScenarioController, 'update_scenario', return_value=[])
    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[])
    def test_put_scenario_json(self, mock_put_scenario, mock_get_all_scenarios):
        client = TestClient(app)
        response = client.put("/?project_id=1&token=1234-1234-1234-1234", json={
            "json": "1",
        })
        assert response.json() == []

    """Testen van PUT uit de view(scenario) op aanroep juiste methode"""

    @mock.patch.object(ScenarioController, 'update_scenario', return_value=[])
    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[])
    def test_put_scenario_calls_correct_method(self, mock_put_scenario, mock_get_all_scenarios):
        client = TestClient(app)
        response = client.put("/?project_id=1&token=1234-1234-1234-1234", json={
            "json": "1",
        })
        mock_put_scenario.assert_called_with(1)

    """Testen van POST uit de view(scenario) op status code 200"""

    @mock.patch.object(ScenarioController, 'update_scenario', return_value=[])
    @mock.patch.object(ScenarioController, 'get_multiple_scenarios_from_ids', return_value=[])
    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[])
    def test_post_scenario(self, mock_update_scenario, get_multiple_scenarios_from_ids, get_all_scenarios):
        client = TestClient(app)
        response = client.post("/?token=1234-1234-1234-1234", json={
            "json": "1",
        })
        assert response.status_code == 200

    """Testen van POST uit de view(scenario) op json return"""

    @mock.patch.object(ScenarioController, 'update_scenario', return_value=[])
    @mock.patch.object(ScenarioController, 'get_multiple_scenarios_from_ids', return_value=[])
    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[])
    def test_post_scenario(self, mock_update_scenario, get_multiple_scenarios_from_ids, get_all_scenarios):
        client = TestClient(app)
        response = client.post("/?project_id=1&token=1234-1234-1234-1234", json={
            "json": "1",
        })
        assert response.json() == []

    """Testen van POST uit de view(scenario) op aanroep juiste methode"""

    @mock.patch.object(ScenarioController, 'create_scenario', return_value=[])
    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[])
    def test_post_scenario(self, mock_get_all_scenarios, mock_create_scenario):
        client = TestClient(app)
        response = client.post("/?project_id=1&token=1234-1234-1234-1234", json={
            "json": "1",
        })
        mock_create_scenario.assert_called_with(ScenarioResponseModel(), 1)
        mock_get_all_scenarios.assert_called_with(1)

    """Testen dat de juiste exception throwed is"""

    @mock.patch.object(ScenarioController, 'get_scenario_from_id', return_value=None)
    def test_get_scenario_from_id(self, mock_get_scenario_from_id):
        client = TestClient(app)
        with self.assertRaises(HTTPException): client.get("/1?project_id=1&token=1234-1234-1234-1234")

    """Testen dat de juiste exception throwed is"""

    @mock.patch.object(ScenarioController, 'get_multiple_scenarios_from_ids', return_value=None)
    def test_get_multiple_scenarios_by_id(self, mock_get_multiple_scenarios_from_ids):
        client = TestClient(app)
        with self.assertRaises(HTTPException): client.post(
            "/selecteer_scenarios?project_id=1&token=1234-1234-1234-1234", json=[])

    """"Testen op return value"""

    @mock.patch.object(ScenarioController, 'get_multiple_scenarios_from_ids', return_value=[1])
    def test_get_multiple_scenarios_by_id_return(self, mock_get_multiple_scenarios_from_ids):
        client = TestClient(app)
        response = client.post("/selecteer_scenarios?project_id=1&token=1234-1234-1234-1234", json=[1]
                               )
        assert response.json() == [ScenarioResponseModel()]

    """"Testen op return value"""

    @mock.patch.object(ScenarioController, 'get_scenario_from_id', return_value=ScenarioResponseModel())
    def test_get_scenario_from_id_return(self, mock_get_scenario_from_id):
        client = TestClient(app)
        response = client.get("/1?project_id=1&token=1234-1234-1234-1234")
        assert response.json() == ScenarioResponseModel()

    """testen of juiste methode wordt gebruikt"""

    @mock.patch.object(ScenarioController, 'add_gebeurtenis_to_scenario', return_value=[])
    def test_add_gebeurtenis_to_scenario(self, mock_add_gebeurtenis):
        client = TestClient(app)
        response = client.post(
            "/1/add_gebeurtenis?project_id=1&gebeurtenis_id=2&project_id=1&token=1234-1234-1234-1234")
        mock_add_gebeurtenis.assert_called_with(1, 2, 1)

    """testen of juiste methode wordt gebruikt"""

    @mock.patch.object(ScenarioController, 'remove_gebeurtenis_from_scenario', return_value=[])
    def test_remove_gebeurtenis_from_scenario(self, mock_remove_gebeurtenis):
        client = TestClient(app)
        response = client.delete("/1/remove_gebeurtenis?gebeurtenis_id=2&project_id=1&token=1234-1234-1234-1234")
        mock_remove_gebeurtenis.assert_called_with(1, 2, 1)

    """testen of juiste methode wordt gebruikt"""

    @mock.patch.object(ScenarioController, 'add_jaar_to_gebeurtenis_in_scenario', return_value=[])
    def test_add_jaar_gebeurtenis(self, mock_add_jaar):
        client = TestClient(app)
        response = client.post("/1/gebeurtenis/2/add_jaar?jaar=3&waarde=4&project_id=1&token=1234-1234-1234-1234")
        mock_add_jaar.assert_called_with(1, 2, 3, 4, 1)

    """testen of juiste methode wordt gebruikt"""

    @mock.patch.object(ScenarioController, 'remove_jaar_from_gebeurtenis_in_scenario', return_value=[])
    def test_remove_jaar_gebeurtenis(self, mock_remove_jaar):
        client = TestClient(app)
        response = client.delete("/1/gebeurtenis/2/remove_jaar?jaar=3&project_id=1&token=1234-1234-1234-1234")
        mock_remove_jaar.assert_called_with(1, 2, 3, 1)

    """testen of juiste methode wordt gebruikt"""

    @mock.patch.object(ScenarioController, 'update_jaar_in_gebeurtenis_in_scenario', return_value=[])
    def test_remove_jaar_gebeurtenis(self, mock_update_jaar):
        client = TestClient(app)
        response = client.put("/1/gebeurtenis/2/update_jaar?jaar=3&waarde=4&project_id=1&token=1234-1234-1234-1234")
        mock_update_jaar.assert_called_with(1, 2, 3, 4, 1)

    @mock.patch.object(ScenarioController, 'remove_jaar_from_gebeurtenis_in_scenario', return_value=[])
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    def test_remove_jaar_from_gebeurtenis_in_scenario(self, mock_can_user_access,
                                                      mock_remove_jaar_from_gebeurtenis_in_scenario):
        # Arrange
        client = TestClient(app)

        # Act
        client.delete("/1/gebeurtenis/1/remove_jaar?jaar=3&project_id=1&token=1234-1234-1234-1234")

        # Assert
        mock_can_user_access.assert_called()
        mock_remove_jaar_from_gebeurtenis_in_scenario.assert_called()

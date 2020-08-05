from datetime import datetime
from unittest import TestCase, mock

import mysql.connector

from app.routers.scenario.scenario_repository import ScenarioMapper, ScenarioJSONParser
from app.routers.scenario.scenario_models import ScenarioResponseModel
from unittest.mock import mock_open, call


class TestScenarioRepo(TestCase):
    """test_db_connection test of de connectie de MySQL connector aanroept"""

    @mock.patch.object(mysql.connector, 'connect', return_value=[])
    def test_db_connection(self, mock_connect):
        mapper = ScenarioMapper()

        mapper._db_connection()

        mock_connect.assert_called()

    """test_data_handler_calls_connection test of de mapper de database connectie aanroept."""

    @mock.patch.object(ScenarioMapper, '_db_connection')
    def test_data_handler_calls_connection(self, mock_db_connection):
        mapper = ScenarioMapper()

        mapper._data_handler("", "", True)

        mock_db_connection.assert_called_with()

    """test_data_handler_returns_None test of de functie data handler niets returnt als de derde parameter False is"""

    @mock.patch.object(ScenarioMapper, '_db_connection')
    def test_data_handler_returns_None(self, mock_db_connection):
        mapper = ScenarioMapper()

        result = mapper._data_handler("", "", False)

        assert result == None

    """test_data_handler_throws_exception test of de data handler functie een exception gooit als er een syntax error 
    in de SQL zit """

    def test_data_handler_throws_exception(self):
        with self.assertRaises(Exception) as excep:
            mapper = ScenarioMapper()
            mapper._data_handler("WRONGQUERY", "", False)

    """test_get_scenarios_returns_list test of de gemockte klasse overeenkomt met het resultaat dat we van de klasse 
    verwachten """

    @mock.patch.object(ScenarioJSONParser, 'get_scenarios_with_details', return_value=[(1, 'Naam', 'Toelichting')])
    def test_scenarios_calls_parser(self, mock_data_handler):
        mapper = ScenarioMapper()
        model = ScenarioResponseModel()
        model.naam = 'Naam'

        scenarios = mapper.get_scenarios(1)

        mock_data_handler.assert_called_with(1)

    """test_add_scenario_calls_data_handler test of de add_scenario de data handler aanroept."""

    @mock.patch.object(ScenarioMapper, '_stored_procedure', return_value=[])
    @mock.patch.object(ScenarioMapper, '_get_scenarios', return_value=[])
    def test_add_scenario_calls_data_handler(self, mock__get_scenarios, mock_stored_procedure):
        model = ScenarioResponseModel()
        mapper = ScenarioMapper()

        mapper.add_scenario(model, 1)

        mock_stored_procedure.assert_called_with('maak_scenario_en_stop_in_project',
                                                 ('scenario', 'toelichting', 1))

    """test_delete_scenario_calls_data_handler test of de delete_scenario de data handler aanroept."""

    @mock.patch.object(ScenarioMapper, '_data_handler', return_value=[])
    @mock.patch.object(ScenarioMapper, '_get_scenarios', return_value=[])
    def test_delete_scenario_calls_data_handler(self, mock__get_scenarios, mock__data_handler):
        mapper = ScenarioMapper()

        mapper.delete_scenario(1, 1)

        mock__data_handler.assert_called_with('DELETE FROM scenario WHERE id = %s', (1,), False)

    """test_update_scenario_calls_data_handler test of de update_scenario de data handler aanroept (twee keer)."""

    @mock.patch.object(ScenarioMapper, '_data_handler', return_value=[])
    @mock.patch.object(ScenarioMapper, '_get_scenarios', return_value=[])
    def test_update_scenario_calls_data_handler(self, mock__get_scenarios, mock__data_handler):
        model = ScenarioResponseModel()
        mapper = ScenarioMapper()

        mapper.update_scenario(model, 1)

        mock__data_handler.assert_called_with("UPDATE scenario " \
                                              "SET naam = %s, toelichting = %s " \
                                              "WHERE id = %s", ('scenario', 'toelichting', 1), False)

    @mock.patch.object(ScenarioMapper, '_data_handler', return_value=[])
    @mock.patch.object(ScenarioMapper, '_get_scenarios', return_value=[])
    def test_add_gebeurtenis_to_scenario_call_data_handler(self, mock__get_scenarios, mock__data_handler):
        # Arrange
        mapper = ScenarioMapper()

        # Act
        mapper.add_gebeurtenis_to_scenario(1, 1, 1)

        # Assert
        mock__data_handler.assert_called()

    @mock.patch.object(ScenarioMapper, '_data_handler', return_value=[])
    @mock.patch.object(ScenarioMapper, '_get_scenarios', return_value=[])
    def test_add_gebeurtenis_to_scenario_call_get_scenarios(self, mock__get_scenarios, mock__data_handler):
        # Arrange
        mapper = ScenarioMapper()

        # Act
        mapper.add_gebeurtenis_to_scenario(1, 1, 1)

        # Assert
        mock__get_scenarios.assert_called()

    @mock.patch.object(ScenarioMapper, '_data_handler', return_value=[])
    @mock.patch.object(ScenarioMapper, '_get_scenarios', return_value=[])
    def test_remove_gebeurtenis_from_scenario_call_data_handler(self, mock__get_scenarios, mock__data_handler):
        # Arrange
        mapper = ScenarioMapper()

        # Act
        mapper.remove_gebeurtenis_from_scenario(1, 1, 1)

        # Assert
        mock__data_handler.assert_called()

    @mock.patch.object(ScenarioMapper, '_data_handler', return_value=[])
    @mock.patch.object(ScenarioMapper, '_get_scenarios', return_value=[])
    def test_remove_gebeurtenis_from_scenario_call_get_scenarios(self, mock__get_scenarios, mock__data_handler):
        # Arrange
        mapper = ScenarioMapper()

        # Act
        mapper.remove_gebeurtenis_from_scenario(1, 1, 1)

        # Assert
        mock__get_scenarios.assert_called()

    @mock.patch.object(ScenarioMapper, '_data_handler', return_value=[])
    @mock.patch.object(ScenarioMapper, '_get_scenarios', return_value=[])
    def test_add_jaar_to_gebeurtenis_in_scenario_call_data_handler(self, mock__get_scenarios, mock__data_handler):
        # Arrange
        mapper = ScenarioMapper()

        # Act
        mapper.add_jaar_to_gebeurtenis_in_scenario(1, 1, 1, 1, 1)

        # Assert
        mock__data_handler.assert_called()

    @mock.patch.object(ScenarioMapper, '_data_handler', return_value=[])
    @mock.patch.object(ScenarioMapper, '_get_scenarios', return_value=[])
    def test_add_jaar_to_gebeurtenis_in_scenario_call_get_scenarios(self, mock__get_scenarios, mock__data_handler):
        # Arrange
        mapper = ScenarioMapper()

        # Act
        mapper.add_jaar_to_gebeurtenis_in_scenario(1, 1, 1, 1, 1)

        # Assert
        mock__get_scenarios.assert_called()

    @mock.patch.object(ScenarioMapper, '_data_handler', return_value=[])
    @mock.patch.object(ScenarioMapper, '_get_scenarios', return_value=[])
    def test_update_jaar_in_gebeurtenis_in_scenario_call_data_handler(self, mock__get_scenarios, mock__data_handler):
        # Arrange
        mapper = ScenarioMapper()

        # Act
        mapper.update_jaar_in_gebeurtenis_in_scenario(1, 1, 1, 1, 1)

        # Assert
        mock__data_handler.assert_called()

    @mock.patch.object(ScenarioMapper, '_data_handler', return_value=[])
    @mock.patch.object(ScenarioMapper, '_get_scenarios', return_value=[])
    def test_update_jaar_in_gebeurtenis_in_scenario_call_get_scenarios(self, mock__get_scenarios, mock__data_handler):
        # Arrange
        mapper = ScenarioMapper()

        # Act
        mapper.update_jaar_in_gebeurtenis_in_scenario(1, 1, 1, 1, 1)

        # Assert
        mock__get_scenarios.assert_called()

    @mock.patch.object(ScenarioMapper, '_data_handler', return_value=[])
    @mock.patch.object(ScenarioMapper, '_get_scenarios', return_value=[])
    def test_remove_jaar_from_gebeurtenis_call_data_handler(self, mock__get_scenarios, mock__data_handler):
        # Arrange
        mapper = ScenarioMapper()

        # Act
        mapper.remove_jaar_from_gebeurtenis(1, 1, 1, 1)

        # Assert
        mock__data_handler.assert_called()

    @mock.patch.object(ScenarioMapper, '_data_handler', return_value=[])
    @mock.patch.object(ScenarioMapper, '_get_scenarios', return_value=[])
    def test_remove_jaar_from_gebeurtenis_call_get_scenarios(self, mock__get_scenarios, mock__data_handler):
        # Arrange
        mapper = ScenarioMapper()

        # Act
        mapper.remove_jaar_from_gebeurtenis(1, 1, 1, 1)

        # Assert
        mock__get_scenarios.assert_called()

    @mock.patch.object(ScenarioJSONParser, 'get_scenarios_with_details', return_value=[])
    def test_get_scenario_by_id_calls_get_scenarios_with_details(self, mock_get_scenarios_with_details):
        # Arrange
        mapper = ScenarioMapper()

        # Act
        mapper.get_scenario_by_id(1, 1)

        # Assert
        mock_get_scenarios_with_details.assert_called()

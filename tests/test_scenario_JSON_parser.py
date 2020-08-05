from unittest import TestCase, mock

from app.routers.overige.overige_repository import JSONParser
from app.routers.scenario.scenario_repository import ScenarioJSONParser


class TestScenarioJSONParser(TestCase):
    test_result = [
        (
            1, 'Edison 70D', '', 1, 1, 1, 1, 0, 1, 1, 'Aanschaf Edison 70D', 'Luxe elektrische auto (sedan)', '',
            'stuk', 1,
            1, 90000.0, 1, 'CAPEX', 'c', '€', 1.0, 'Capital Expenditure (investeringen)'),
        (1, 'Edison 70D', '', 1, 19, 6, 6, 8, 8, 19, 'Nieuwe banden (sedan)', 'Vervangen van banden na 60.000 Km', '',
         'stuk', 19, 1, 100.0, 1, 'CAPEX', 'c', '€', 1.0, 'Capital Expenditure (investeringen)'),
        (1, 'Edison 70D', '', 1, 19, 6, 6, 16, 8, 19, 'Nieuwe banden (sedan)', 'Vervangen van banden na 60.000 Km', '',
         'stuk', 19, 1, 100.0, 1, 'CAPEX', 'c', '€', 1.0, 'Capital Expenditure (investeringen)'),
        (1, 'Edison 70D', '', 1, 26, 9, 9, 20, 1, 26, 'Verkoop van Edison 70D',
         'Restwaarde bij verkoop als tweedehands auto', '', 'keer', 26, 1, -9000.0, 1, 'CAPEX', 'c', '€', 1.0,
         'Capital Expenditure (investeringen)')
    ]

    @mock.patch.object(JSONParser, '_data_handler', return_value=test_result)
    def test_returns_calls_data_handler(self, data_handler):
        parser = ScenarioJSONParser()

        parser.get_scenarios_with_details(1)

        data_handler.assert_called_with(
            'SELECT * FROM scenario s LEFT JOIN scenario_gebeurtenis sg ON s.id = sg.scenario_id LEFT JOIN jaren j ON sg.koppeling_id = j.koppeling_id LEFT JOIN gebeurtenis g ON g.id = sg.gebeurtenis_id LEFT JOIN gebeurtenis_interventie gi ON gi.gebeurtenis_id = g.id LEFT JOIN interventie i ON gi.interventie_id = i.id LEFT JOIN project_scenario ps ON s.id = ps.scenario_id WHERE ps.project_id = %s ORDER BY s.id, g.id',
            (1,), True)

    @mock.patch.object(JSONParser, '_data_handler', return_value=test_result)
    def test_call_all_returns_calls_data_handler(self, data_handler):
        parser = ScenarioJSONParser()

        parser.get_scenarios_with_details(1)

        data_handler.assert_called_with(
            'SELECT * FROM scenario s LEFT JOIN scenario_gebeurtenis sg ON s.id = sg.scenario_id LEFT JOIN jaren j ON sg.koppeling_id = j.koppeling_id LEFT JOIN gebeurtenis g ON g.id = sg.gebeurtenis_id LEFT JOIN gebeurtenis_interventie gi ON gi.gebeurtenis_id = g.id LEFT JOIN interventie i ON gi.interventie_id = i.id LEFT JOIN project_scenario ps ON s.id = ps.scenario_id WHERE ps.project_id = %s ORDER BY s.id, g.id',
            (1,), True)

    @mock.patch.object(JSONParser, '_data_handler', return_value=[])
    def test_returns_nothing_if_no_data(self, data_handler):
        parser = ScenarioJSONParser()

        result = parser.get_scenarios_with_details(-1)

        assert result == []

    @mock.patch.object(JSONParser, '_data_handler', return_value=[])
    def test_get_all_returns_nothing_if_no_data(self, data_handler):
        parser = ScenarioJSONParser()

        result = parser.get_scenarios_with_details(1)
        print(result)

        assert result == []

    @mock.patch.object(JSONParser, '_data_handler', return_value=[])
    def test__get_results_for_scenarios(self, mock__data_handler):
        # Arrange
        parser = ScenarioJSONParser()
        query = "SELECT * FROM scenario s JOIN scenario_gebeurtenis sg ON s.id = sg.scenario_id JOIN jaren j " \
                "ON sg.koppeling_id = j.koppeling_id JOIN gebeurtenis g ON g.id = sg.gebeurtenis_id " \
                "JOIN gebeurtenis_interventie gi ON gi.gebeurtenis_id = g.id JOIN interventie i " \
                "ON gi.interventie_id = i.id JOIN project_scenario ps ON ps.scenario_id = s.id WHERE s.id = %s AND ps.scenario_id = %s " \
                "ORDER BY s.id, g.id"
        scenario_id = 1
        project_id = 1

        # Act
        parser._get_results_for_scenarios(scenario_id, project_id)

        # Assert
        mock__data_handler.assert_called_with(query, (scenario_id, project_id), True)

from unittest import TestCase, mock

from app.routers.overige.overige_repository import JSONParser
from app.routers.gebeurtenis.gebeurtenis_repository import GebeurtenisJSONParser


class TestGebeurtenisJSONParser(TestCase):
    """get_all_calls_data_handler test of de juiste query naar de server wordt gestuurd"""

    @mock.patch.object(JSONParser, '_data_handler', return_value=[])
    def test_get_all_calls_data_handler(self, data_handler):
        parser = GebeurtenisJSONParser()

        parser.get_gebeurtenissen(1)

        data_handler.assert_called_with(
            'SELECT * FROM gebeurtenis g LEFT JOIN gebeurtenis_interventie gi on g.id = gi.gebeurtenis_id LEFT JOIN interventie i on gi.interventie_id = i.id LEFT JOIN  project_gebeurtenis pg ON pg.gebeurtenis_id = g.id WHERE pg.project_id = %s',
            (1,), True)

    """get_all_returns_none_without_results checkt of de methode een lege lijst returnt als de database leeg is"""

    @mock.patch.object(JSONParser, '_data_handler', return_value=[])
    def test_get_gebeurtenis_returns_none_without_results(self, data_handler):
        parser = GebeurtenisJSONParser()

        result = parser.get_gebeurtenissen(1)

        assert result == []

    @mock.patch.object(JSONParser, '_data_handler', return_value=[])
    def test_get_one_calls_handler(self, data_handler):
        parser = GebeurtenisJSONParser()

        parser.get_gebeurtenissen(1)

        data_handler.assert_called_with(
            'SELECT * FROM gebeurtenis g LEFT JOIN gebeurtenis_interventie gi on g.id = gi.gebeurtenis_id LEFT JOIN interventie i on gi.interventie_id = i.id LEFT JOIN  project_gebeurtenis pg ON pg.gebeurtenis_id = g.id WHERE pg.project_id = %s',
            (1,), True)

    @mock.patch.object(JSONParser, '_data_handler', return_value=[
        (1, 'Aanschaf Edison 70D', 'Luxe elektrische auto (sedan)', '', 'stuk', 1, 1, 90000.0, 1, 'CAPEX', 'c', '€',
         1.0, 'Capital Expenditure (investeringen)'), (
                1, 'Aanschaf Edison 70D', 'Luxe elektrische auto (sedan)', '', 'stuk', 1, 4, 17000.0, 4, 'CO2-Uitstoot',
                'w',
                'ton CO2 eq.', 0.11, 'Milleuschade door emissies van CO2 in atmosfeer')])
    def test_get_one_returns_list(self, data_handler):
        parser = GebeurtenisJSONParser()

        result = parser.get_gebeurtenissen(1)

        assert result[0].naam == "Aanschaf Edison 70D"

    @mock.patch.object(JSONParser, '_data_handler', return_value=[])
    def test__get_queries_calls_data_handler(self, mock__data_handler):
        # Arrange
        parser = GebeurtenisJSONParser()
        query = "SELECT * FROM gebeurtenis g LEFT JOIN gebeurtenis_interventie gi on g.id = gi.gebeurtenis_id LEFT JOIN interventie i on gi.interventie_id = i.id WHERE g.id = %s"
        gebeurtenis_id = 1

        # Act
        parser._get_queries(gebeurtenis_id, 1)

        # Assert
        mock__data_handler.assert_called()

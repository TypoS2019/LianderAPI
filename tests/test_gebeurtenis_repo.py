from unittest import TestCase, mock

import mysql.connector

from app.routers.overige.overige_repository import JSONParser
from app.routers.scenario.scenario_repository import ScenarioMapper
from app.routers.scenario.scenario_models import ScenarioResponseModel
from unittest.mock import mock_open, call

from app.routers.gebeurtenis.gebeurtenis_models import GebeurtenisResponseModel
from app.routers.gebeurtenis.gebeurtenis_repository import GebeurtenisMapper, GebeurtenisJSONParser


class TestGebeurtenisRepo(TestCase):
    @mock.patch.object(mysql.connector, 'connect', return_value=[])
    def test_db_connection(self, mock_connect):
        mapper = GebeurtenisMapper()

        mapper._db_connection()

        mock_connect.assert_called()

    @mock.patch.object(GebeurtenisMapper, '_db_connection')
    def test_data_handler_calls_connection(self, mock_db_connection):
        mapper = GebeurtenisMapper()

        mapper._data_handler("", "", True)

        mock_db_connection.assert_called_with()

    @mock.patch.object(GebeurtenisMapper, '_db_connection')
    def test_data_handler_returns_None(self, mock_db_connection):
        mapper = GebeurtenisMapper()

        result = mapper._data_handler("", "", False)

        assert result == None

    def test_data_handler_throws_exception(self):
        with self.assertRaises(Exception) as excep:
            mapper = GebeurtenisMapper()
            mapper._data_handler("WRONGQUERY", "", False)

    @mock.patch.object(JSONParser, '_data_handler', return_value=[
        (1, 'Aanschaf Edison 70D', 'Luxe elektrische auto (sedan)', '', 'stuk', 1, 1, 90000.0, 1, 'CAPEX', 'c', '€',
         1.0, 'Capital Expenditure (investeringen)'), (
                1, 'Aanschaf Edison 70D', 'Luxe elektrische auto (sedan)', '', 'stuk', 1, 4, 17000.0, 4, 'CO2-Uitstoot',
                'w',
                'ton CO2 eq.', 0.11, 'Milleuschade door emissies van CO2 in atmosfeer')])
    def test_get_gebeurtenis_returns_list(self, mock_data_handler):
        mapper = GebeurtenisMapper()
        model = GebeurtenisResponseModel()
        model.naam = 'Aanschaf Edison 70D'
        project_id = 1
        gebeurtenissen = mapper.get_gebeurtenissen(project_id)

        print(gebeurtenissen[0].naam)

        assert gebeurtenissen[0].naam == model.naam

    @mock.patch.object(GebeurtenisMapper, '_stored_procedure', return_value=[])
    @mock.patch.object(GebeurtenisMapper, 'get_gebeurtenissen', return_value=[])
    def test_add_gebeurtenis_calls_data_handler(self, mock_get_gebeurtenissen, mock_stored_procedure):
        model = GebeurtenisResponseModel()
        mapper = GebeurtenisMapper()
        project_id = 1
        mapper.add_gebeurtenis(model, project_id)

        mock_stored_procedure.assert_called_with('maak_gebeurtenis_en_stop_in_project',
                                                 ('naam', 'toelichting', 'bronvermelding', 'eenheid_per', 1))

    @mock.patch.object(GebeurtenisMapper, '_data_handler', return_value=[])
    @mock.patch.object(GebeurtenisMapper, 'get_gebeurtenissen', return_value=[])
    def test_delete_gebeurtenis_calls_data_handler(self, mock_get_gebeurtenissen, mock__data_handler):
        mapper = GebeurtenisMapper()
        project_id = 1
        mapper.delete_gebeurtenis(1, project_id)

        mock__data_handler.assert_called_with('DELETE FROM gebeurtenis WHERE id = %s', (1,), False)

    @mock.patch.object(GebeurtenisMapper, '_data_handler', return_value=[])
    @mock.patch.object(GebeurtenisMapper, 'get_gebeurtenissen', return_value=[])
    def test_update_gebeurtenis_calls_data_handler(self, mock_get_gebeurtenissen, mock__data_handler):
        model = GebeurtenisResponseModel()
        mapper = GebeurtenisMapper()
        project_id = 1
        mapper.update_gebeurtenis(model, project_id)

        mock__data_handler.assert_called_with(
            'UPDATE gebeurtenis SET naam = %s, toelichting = %s, bron = %s, eenheid = %s WHERE id = %s',
            ('naam', 'toelichting', 'bronvermelding', 'eenheid_per', 1), False)

    @mock.patch.object(GebeurtenisMapper, 'get_gebeurtenissen', return_value=[])
    @mock.patch.object(GebeurtenisMapper, '_data_handler', return_value=[])
    def test_add_interventie_to_gebeurtenis_calls__data_handler(self, mock__data_handler, mock_get_gebeurtenissen):
        # Arrange
        mapper = GebeurtenisMapper()

        # Act
        mapper.add_interventie_to_gebeurtenis(1, 1, 1)

        # Assert
        mock__data_handler.assert_called()

    @mock.patch.object(GebeurtenisMapper, 'get_gebeurtenissen', return_value=[])
    @mock.patch.object(GebeurtenisMapper, '_data_handler', return_value=[])
    def test_add_interventie_to_gebeurtenis_calls_get_gebeurtenissen(self, mock__data_handler, mock_get_gebeurtenissen):
        # Arrange
        mapper = GebeurtenisMapper()

        # Act
        mapper.add_interventie_to_gebeurtenis(1, 1, 1)

        # Assert
        mock_get_gebeurtenissen.assert_called()

    @mock.patch.object(GebeurtenisMapper, 'get_gebeurtenissen', return_value=[])
    @mock.patch.object(GebeurtenisMapper, '_data_handler', return_value=[])
    def test_update_interventie_in_gebeurtenis_calls__data_handler(self, mock__data_handler, mock_get_gebeurtenissen):
        # Arrange
        mapper = GebeurtenisMapper()

        # Act
        mapper.update_interventie_in_gebeurtenis(1, 1, 1, 1)

        # Assert
        mock__data_handler.assert_called()

    @mock.patch.object(GebeurtenisMapper, 'get_gebeurtenissen', return_value=[])
    @mock.patch.object(GebeurtenisMapper, '_data_handler', return_value=[])
    def test_update_interventie_in_gebeurtenis_calls_get_gebeurtenissen(self, mock__data_handler, mock_get_gebeurtenissen):
        # Arrange
        mapper = GebeurtenisMapper()

        # Act
        mapper.update_interventie_in_gebeurtenis(1, 1, 1, 1)

        # Assert
        mock_get_gebeurtenissen.assert_called()

    @mock.patch.object(GebeurtenisMapper, 'get_gebeurtenissen', return_value=[])
    @mock.patch.object(GebeurtenisMapper, '_data_handler', return_value=[])
    def test_remove_interventie_from_gebeurtenis_calls__data_handler(self, mock__data_handler, mock_get_gebeurtenissen):
        # Arrange
        mapper = GebeurtenisMapper()

        # Act
        mapper.remove_interventie_from_gebeurtenis(1, 1, 1)

        # Assert
        mock__data_handler.assert_called()

    @mock.patch.object(GebeurtenisMapper, 'get_gebeurtenissen', return_value=[])
    @mock.patch.object(GebeurtenisMapper, '_data_handler', return_value=[])
    def test_remove_interventie_from_gebeurtenis_calls_get_gebeurtenissen(self, mock__data_handler,
                                                                        mock_get_gebeurtenissen):
        # Arrange
        mapper = GebeurtenisMapper()

        # Act
        mapper.remove_interventie_from_gebeurtenis(1, 1, 1)

        # Assert
        mock_get_gebeurtenissen.assert_called()



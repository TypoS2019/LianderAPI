from unittest import TestCase, mock

import mysql.connector

from unittest.mock import mock_open, call

from app.routers.interventie.interventie_models import InterventieResponseModel
from app.routers.interventie.interventie_repository import InterventieMapper
from app.routers.overige.overige_repository import DataMapper


class TestInterventieRepo(TestCase):
    """test_db_connection test of de connectie de MySQL connector aanroept"""

    @mock.patch.object(mysql.connector, 'connect', return_value=[])
    def test_db_connection(self, mock_connect):
        mapper = InterventieMapper()

        mapper._db_connection()

        mock_connect.assert_called()

    """test_data_handler_calls_connection test of de mapper de database connectie aanroept."""

    @mock.patch.object(InterventieMapper, '_db_connection')
    def test_data_handler_calls_connection(self, mock_db_connection):
        mapper = InterventieMapper()

        mapper._data_handler("", "", True)

        mock_db_connection.assert_called_with()

    """test_data_handler_returns_None test of de functie data handler niets returnt als de derde parameter False is"""

    @mock.patch.object(InterventieMapper, '_db_connection')
    def test_data_handler_returns_None(self, mock_db_connection):
        mapper = InterventieMapper()

        result = mapper._data_handler("", "", False)

        assert result == None

    """test_data_handler_throws_exception test of de data handler functie een exception gooit als er een syntax error in de SQL zit"""

    def test_data_handler_throws_exception(self):
        with self.assertRaises(Exception) as excep:
            mapper = InterventieMapper()
            mapper._data_handler("WRONGQUERY", "", False)

    """test_get_scenarios_returns_list test of de gemockte klasse overeenkomt met het resultaat dat we van de klasse verwachten"""

    @mock.patch.object(InterventieMapper, '_data_handler',
                       return_value=[(1, 'Naam', 'Type', 'Eenheid', 'Waarde', 'Toelichting')])
    def test_get_interventies_returns_list(self, mock_data_handler):
        mapper = InterventieMapper()
        model = InterventieResponseModel()
        model.naam = 'Naam'
        project_id = 1
        scenarios = mapper._get_interventies(project_id)

        assert scenarios[0].naam == model.naam

    """test_add_scenario_calls_data_handler test of de add_scenario de data handler aanroept."""

    @mock.patch.object(DataMapper, '_stored_procedure', return_value="return-value")
    @mock.patch.object(InterventieMapper, '_data_handler', return_value=[])
    def test_add_interventie_calls_data_handler(self, mock__data_handler, mocked_stored_procedure):
        model = InterventieResponseModel()
        mapper = InterventieMapper()
        project_id = 1
        mapper.add_interventie(model, project_id)

        mocked_stored_procedure.assert_called_with('maak_interventie_en_stop_in_project', ('CAPEX', 'c', '$', 1, 'toelichting', 1))

    """test_delete_scenario_calls_data_handler test of de delete_scenario de data handler aanroept."""

    @mock.patch.object(InterventieMapper, '_data_handler', return_value=[])
    def test_delete_interventie_calls_data_handler(self, mock__data_handler):
        mapper = InterventieMapper()
        project_id = 1
        mapper.delete_interventie(1, project_id)

        mock__data_handler.assert_has_calls([call('DELETE FROM interventie WHERE id = %s', (1,), False),
                                             call('SELECT * FROM interventie i LEFT JOIN project_interventie pi on pi.interventie_id = i.id WHERE pi.project_id = %s',
                                                 (1,), True)])

    """test_get_interventie_calls_data_handler test of het ID dat opgevraagd wordt ook daadwerkelijk teruggegeven wordt"""

    @mock.patch.object(InterventieMapper, '_data_handler',
                       return_value=[(1, 'Naam', 'Type', 'Eenheid', 'Waarde', 'Toelichting')])
    def test_get_interventie_calls_data_handler(self, mock__data_handler):
        mapper = InterventieMapper()
        project_id = 1
        result = mapper.get_interventie(1, project_id)

        assert result.id == 1

    """test_get_interventies_calls_handler test of de data handler aangeroepen wordt"""

    @mock.patch.object(InterventieMapper, '_data_handler',
                       return_value=[])
    def test_get_interventies_calls_handler(self, mock__data_handler):
        mapper = InterventieMapper()
        project_id = 1
        result = mapper.get_interventies(project_id)

        mock__data_handler.assert_called_with('SELECT * FROM interventie i LEFT JOIN project_interventie pi on pi.interventie_id = i.id WHERE pi.project_id = %s', (1,), True)

    """test_get_interventie_returns_none test of de functie None returnt als het ID niet is gevonden """

    @mock.patch.object(InterventieMapper, '_data_handler',
                       return_value=[])
    def test_get_interventie_returns_none(self, mock__data_handler):
        mapper = InterventieMapper()
        project_id = 1
        result = mapper.get_interventie(1, project_id)

        assert result is None

    """test_update_scenario_calls_data_handler test of de update_scenario de data handler aanroept (twee keer)."""

    @mock.patch.object(InterventieMapper, '_data_handler', return_value=[])
    def test_update_scenario_calls_data_handler(self, mock__data_handler):
        model = InterventieResponseModel()
        mapper = InterventieMapper()
        project_id = 1
        mapper.update_interventie(model, project_id)

        mock__data_handler.assert_has_calls([call('UPDATE interventie SET naam = %s, type = %s, eenheid = %s, waarde = %s, toelichting = %s WHERE id = %s', ('CAPEX', 'c', '$', 1, 'toelichting', 1), False),
 call('SELECT * FROM interventie i LEFT JOIN project_interventie pi on pi.interventie_id = i.id WHERE pi.project_id = %s', (project_id,), True)])

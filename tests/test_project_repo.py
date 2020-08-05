import datetime
from unittest import TestCase, mock

import mysql.connector

from app.routers.overige.overige_repository import JSONParser
from app.routers.project.project_controller import ProjectController
from app.routers.project.project_models import ProjectResponseModel
from unittest.mock import mock_open, call

from app.routers.gebeurtenis.gebeurtenis_models import GebeurtenisResponseModel
from app.routers.project.project_repository import ProjectMapper


class TestProjectRepo(TestCase):

    def setUp(self):
        self.project_controller = ProjectController()
        self.project_mapper = ProjectMapper()
        self.test_model = ProjectResponseModel()
        self.test_token = "12345"
        self.test_id = 1

    """test_db_connection test of de database verbinding wordt aangeroepen"""

    @mock.patch.object(mysql.connector, 'connect', return_value=[])
    def test_db_connection(self, mock_connect):
        self.project_mapper._db_connection()

        mock_connect.assert_called()

    """test_data_handler_calls_connection test of de data_handler de database verbinding aanroept"""

    @mock.patch.object(ProjectMapper, '_db_connection')
    def test_data_handler_calls_connection(self, mock_db_connection):
        self.project_mapper._data_handler("", "", True)

        mock_db_connection.assert_called_with()

    """test_data_handler_returns_none controleert of de data_handler het juiste retourneert"""

    @mock.patch.object(ProjectMapper, '_db_connection')
    def test_data_handler_returns_None(self, mock_db_connection):
        result = self.project_mapper._data_handler("", "", False)

        assert result == None

    """test_data_handler_throws_exception controleert of de data_handler een exception gooit wanneer er een verkeerde 
    query wordt ingevoerd """

    def test_data_handler_throws_exception(self):
        with self.assertRaises(Exception) as excep:
            self.project_mapper._data_handler("WRONGQUERY", "", False)

    """test_get_projecten_returns_list test of get_alle_projecten de juiste data retourneert"""

    @mock.patch.object(ProjectMapper, '_get_projecten', return_value=[ProjectResponseModel()])
    @mock.patch.object(JSONParser, '_data_handler', return_value=[])
    def test_get_projecten_returns_list(self, mock_data_handler, mock__get_projecten):
        projecten = self.project_mapper.get_alle_projecten('test_gebruiker')

        assert projecten == [self.test_model]

    """test_get_project_returns_model test of get_project het gewenste project retourneert"""

    @mock.patch.object(ProjectMapper, '_get_projecten', return_value=[ProjectResponseModel()])
    @mock.patch.object(JSONParser, '_data_handler', return_value=[])
    def test_get_project_returns_model(self, mock_data_handler, mock__get_projecten):
        project = self.project_mapper.get_project(self.test_id)

        assert project == self.test_model

    @mock.patch.object(ProjectMapper, '_get_projecten', return_value=[])
    @mock.patch.object(JSONParser, '_data_handler', return_value=[])
    def test_get_project_returns_None_when_list_is_empty(self, mock_data_handler, mock__get_projecten):
        project = self.project_mapper.get_project(self.test_id)

        assert project is None

    """test_add_project_calls_data_handler test of de methode add_project de data_handler correct aanroept"""

    @mock.patch.object(ProjectMapper, '_get_current_date',
                       return_value=datetime.datetime(2019, 12, 17, 11, 40, 27, 793131))
    @mock.patch.object(ProjectMapper, '_data_handler', return_value=[])
    def test_add_project_calls_data_handler(self, mock__data_handler, mock__get_current_date):
        self.project_mapper.add_project(self.test_model, self.test_token)
        mock__data_handler.assert_called_with(
            'INSERT INTO project_gebruiker (gebruiker_id, project_id) VALUES (%s, %s)', ('12345', None), False)

    """test_update_project_calls_data_handler test of de methode update_project de data_handler correct aanroept"""

    @mock.patch.object(ProjectMapper, '_get_projecten', return_value=[ProjectResponseModel()])
    @mock.patch.object(ProjectMapper, '_data_handler', return_value=[])
    def test_update_project_calls_data_handler(self, mock__data_handler, mock__get_projecten):
        self.project_mapper.update_project(self.test_model)
        mock__data_handler.assert_called_with(
            "UPDATE project SET naam = %s, datum = %s WHERE id = %s",
            (self.test_model.naam, self.test_model.datum, self.test_model.id),
            False)

    """test_delete_project_calls_data_handler test of de methode delete_project de data_handler corrrect aanroept"""

    @mock.patch.object(ProjectMapper, '_data_handler', return_value=[])
    def test_delete_project_calls_data_handler(self, mock__data_handler):
        self.project_mapper.delete_project(self.test_id)
        mock__data_handler.assert_called_with(
            "DELETE FROM project WHERE id = %s", (self.test_id,), False)

    def test__get_current_date_returns_correct_date(self):
        # Arrange
        date = datetime.datetime.now()

        # Act
        output = self.project_mapper._get_current_date()

        # Assert
        assert output.hour == date.hour

    @mock.patch.object(ProjectMapper, '_data_handler', return_value=[])
    def test_voeg_gebruiker_toe_aan_project_calls_data_handler(self, mock__data_handler):
        # Act
        self.project_mapper.voeg_gebruiker_toe_aan_project(1, 1)

        # Assert
        mock__data_handler.assert_called()

    @mock.patch.object(ProjectMapper, '_data_handler', return_value=[])
    def test_verwijder_gebruiker_uit_project_calls_data_handler(self, mock__data_handler):
        # Act
        self.project_mapper.verwijder_gebruiker_uit_project(1, 1, "1")

        # Assert
        mock__data_handler.assert_called()

    @mock.patch.object(ProjectMapper, '_data_handler', return_value=[])
    def test_get_projecten_calls_data_handler(self, mock__data_handler):
        # Act
        self.project_mapper._get_projecten('test_gebruiker')

        # Assert
        mock__data_handler.assert_called()

    @mock.patch.object(ProjectMapper, '_data_handler', return_value=[ProjectResponseModel().json()])
    def test_get_projecten_returns_list_with_correct_length(self, mock__data_handler):
        # Act
        output = self.project_mapper._get_projecten('test_gebruiker')

        # Assert
        assert len(output) == 1

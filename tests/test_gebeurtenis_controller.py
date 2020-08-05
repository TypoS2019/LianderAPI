from typing import List
from unittest import TestCase

import mock
from app.routers.gebeurtenis.gebeurtenis_models import GebeurtenisResponseModel
from app.routers.gebeurtenis.gebeurtenis_controller import GebeurtenisController
from app.routers.gebeurtenis.gebeurtenis_repository import GebeurtenisMapper


class TestGebeurtenisController(TestCase):

    def setUp(self):
        self.gebeurtenis_controller = GebeurtenisController()

    """test_get_gebeurtenissen_calls_corret_method_from_repository test of de  methode get_gebeurtenissen in de 
    controller correct werkt. """
    @mock.patch.object(GebeurtenisMapper, 'get_gebeurtenissen', return_value=[])
    def test_get_gebeurtenissen_calls_correct_method_from_repository(self, mock_get_gebeurtenissen):
        project_id = 1
        self.gebeurtenis_controller.get_gebeurtenissen(project_id)
        mock_get_gebeurtenissen.assert_called_with(project_id)  # check of get_gebeurtenissen in de repository wordt aangeroepen

    """test_delete_gebeurtenis_calls_correct_method_from_repository test of de  methode delete_gebeurtenis in de 
    controller correct werkt. """
    @mock.patch.object(GebeurtenisMapper, 'delete_gebeurtenis', return_value=[])
    def test_delete_gebeurtenis_calls_correct_method_from_repository(self, mock_delete_gebeurtenis):
        project_id = 1
        self.gebeurtenis_controller.delete_gebeurtenis(1, project_id)
        mock_delete_gebeurtenis.assert_called_with(1, project_id)  # check of delete_gebeurtenis in de repository wordt aangeroepen

    """test_update_gebeurtenis_calls_correct_method_from_repository test of de  methode update_gebeurtenis in de 
        controller correct werkt. """
    @mock.patch.object(GebeurtenisMapper, 'update_gebeurtenis', return_value=[])
    def test_update_gebeurtenis_calls_correct_method_from_repository(self, mock_update_gebeurtenis):
        project_id = 1
        self.gebeurtenis_controller.update_gebeurtenis(GebeurtenisResponseModel, project_id)
        mock_update_gebeurtenis.assert_called_with(GebeurtenisResponseModel, project_id)
        # ↑ check of update_gebeurtenis in de repository wordt aangeroepen

    """test_add_gebeurtenis_calls_correct_method_from_repository test of de  methode update_gebeurtenis in de 
        controller correct werkt. """
    @mock.patch.object(GebeurtenisMapper, 'add_gebeurtenis', return_value=[])
    @mock.patch.object(GebeurtenisMapper, 'get_gebeurtenissen', return_value=[])
    def test_add_gebeurtenis_calls_correct_method_from_repository(self, mock_add_gebeurtenis,
                                                                  mock_get_gebeurtenissen):
        project_id = 1
        self.gebeurtenis_controller.post_gebeurtenis(GebeurtenisResponseModel, project_id)
        mock_add_gebeurtenis.assert_called_with(project_id)  # check of add_gebeurtenis in de repository wordt aangeroepen

    """test_add_interventie_to_gebeurtenis test of de methode correct werkt in de controller"""
    @mock.patch.object(GebeurtenisMapper, 'add_interventie_to_gebeurtenis', return_value=[])
    def test_add_interventie_to_gebeurtenis(self, mock_add_interventie_gebeurtenis):
        gebeurtenis_id = 1
        interventie_id = 2
        project_id = 1
        self.gebeurtenis_controller.add_interventie_to_gebeurtenis(gebeurtenis_id, interventie_id, project_id)
        mock_add_interventie_gebeurtenis.assert_called_with(gebeurtenis_id, interventie_id, project_id)

    """test_update_interventie_in_gebeurtenis test of  de methode correct werkt in de controller"""
    @mock.patch.object(GebeurtenisMapper, 'update_interventie_in_gebeurtenis', return_value=[])
    def test_update_interventie_in_gebeurtenis(self, mock_update_interventie_gebeurtenis):
        gebeurtenis_id = 1
        interventie_id = 2
        waarde = 3
        project_id = 1
        self.gebeurtenis_controller.update_interventie_in_gebeurtenis(gebeurtenis_id, interventie_id, waarde, project_id)
        mock_update_interventie_gebeurtenis.assert_called_with(gebeurtenis_id, interventie_id, waarde, project_id)

    """test_remove_interventie_from_gebeurtenis test of de methode remove_interventie_from_gebeurtenis in de 
        controller correct werken"""
    @mock.patch.object(GebeurtenisMapper, 'remove_interventie_from_gebeurtenis', return_value=[])
    def test_remove_interventie_from_gebeurtenis(self, mock_remove_interventie_gebeurtenis):
        gebeurtenis_id = 1
        interventie_id = 2
        project_id = 1
        self.gebeurtenis_controller.remove_interventie_from_gebeurtenis(gebeurtenis_id, interventie_id, project_id)
        mock_remove_interventie_gebeurtenis.assert_called_with(gebeurtenis_id, interventie_id, project_id)
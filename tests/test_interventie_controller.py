from unittest import TestCase, mock

from app.routers.interventie.interventie_controller import InterventieController
from app.routers.interventie.interventie_models import InterventieResponseModel
from app.routers.interventie.interventie_repository import InterventieMapper


class TestInterventieController(TestCase):

    def setUp(self):
        self.interventie_controller = InterventieController()

    """Testen of test_update_interventie_method_call_controller de  methode update_interventie in de 
        controller correct aanroept"""

    @mock.patch.object(InterventieMapper, 'update_interventie', return_value=[])
    def test_update_interventie_method_call_controller(self, mock_update_interventie):
        project_id = 1
        self.interventie_controller.update_interventie(InterventieResponseModel, project_id)
        mock_update_interventie.assert_called_with(InterventieResponseModel, project_id)

    """Testen of test_add_interventie_method_call_controller de methode add_interventie 
    in de controller correct aanroept"""

    @mock.patch.object(InterventieMapper, 'add_interventie', return_value=[])
    def test_add_interventie_method_call_controller(self, mock_add_interventie):
        project_id = 1
        self.interventie_controller.create_interventie(InterventieResponseModel, project_id)
        mock_add_interventie.assert_called_with(InterventieResponseModel, project_id)

    """Testen of test_get_interventies_method_call_controller de methode add_interventie 
        in de controller correct aanroept"""

    @mock.patch.object(InterventieMapper, 'get_interventies', return_value=[])
    def test_get_interventies_method_call_controller(self, mock_get_interventies):
        project_id = 1
        self.interventie_controller.get_interventies(project_id)
        mock_get_interventies.assert_called_with(project_id)

    """Testen of test_get_interventie_method_call_controller de methode add_interventie 
            in de controller correct aanroept"""

    @mock.patch.object(InterventieMapper, 'get_interventie', return_value=[])
    def test_get_interventie_method_call_controller(self, mock_get_interventie):
        project_id = 1
        self.interventie_controller.get_interventie(1, project_id)
        mock_get_interventie.assert_called_with(1, project_id)

    @mock.patch.object(InterventieMapper, 'delete_interventie', return_value=[])
    def test_delete_interventie_calls_interventie_mapper_delete_interventie(self, mock_delete_interventie):
        # Act
        self.interventie_controller.delete_interventie(1, 1)

        # Assert
        mock_delete_interventie.assert_called()

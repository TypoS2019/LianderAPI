from unittest import TestCase, mock

from app.routers.project.project_controller import ProjectController
from app.routers.project.project_models import ProjectResponseModel
from app.routers.project.project_repository import ProjectMapper


class TestProjectController(TestCase):

    def setUp(self):
        self.project_controller = ProjectController()
        self.test_model = ProjectResponseModel()
        self.test_token = "12345"
        self.test_id = 1

    """test_create_project_calls_correct_method test of de functie create_project de correcte methode aanroept"""

    @mock.patch.object(ProjectMapper, 'add_project', return_value="")
    def test_create_project_calls_correct_method(self, mock_add_project):
        self.project_controller.create_project(self.test_model, self.test_token)
        mock_add_project.assert_called_with(self.test_model, self.test_token)

    """test_get_alle_projecten_calls_correct_method test of de functie get_alle_projecten de correcte methode 
    aanroept """

    @mock.patch.object(ProjectMapper, 'get_alle_projecten', return_value="")
    def test_get_alle_projecten_calls_correct_method(self, mock_get_alle_projecten):
        self.project_controller.get_alle_projecten(self.test_token)
        mock_get_alle_projecten.assert_called_with(self.test_token)

    """test_get_project_by_id_calls_correct_method test of de functie get_project_by_id de correcte methode aanroept"""

    @mock.patch.object(ProjectMapper, 'get_project', return_value="")
    def test_get_project_by_id_calls_correct_method(self, mock_get_project):
        self.project_controller.get_project_by_id(self.test_id, self.test_token)
        mock_get_project.assert_called_with(self.test_id)

    """test_delete_project_calls_correct_method test of de functie delete_project de correcte methode aanroept"""

    @mock.patch.object(ProjectMapper, 'delete_project', return_value="")
    def test_delete_project_calls_correct_method(self, mock_delete_project):
        self.project_controller.delete_project(self.test_id, self.test_token)
        mock_delete_project.assert_called_with(self.test_id)

    """test_update_project_calls_correct_method test of de functie update_project de correcte methode aanroept"""

    @mock.patch.object(ProjectMapper, 'update_project', return_value="")
    def test_update_project_calls_correct_method(self, mock_update_project):
        self.project_controller.update_project(self.test_model, self.test_token)
        mock_update_project.assert_called_with(self.test_model)

    """test_voeg_gebruiker_toe_aan_project_calls_correct_method test of de functie voeg_gebruiker_toe_aan_project de 
    correcte methode aanroept """

    @mock.patch.object(ProjectMapper, 'voeg_gebruiker_toe_aan_project', return_value="")
    # testfunctie, deze later vervangen door echte functie
    def test_voeg_gebruiker_toe_aan_project_calls_correct_method(self, voeg_gebruiker_toe_aan_project):
        self.project_controller.voeg_gebruiker_toe_aan_project(self.test_id, self.test_id, self.test_token)
        voeg_gebruiker_toe_aan_project.assert_called_with(1, 1)

    """test_verwijder_gebruiker_uit_project_calls_correct_method test of de functie verwijder_gebruiker_uit_project 
    de correcte methode aanroept """

    @mock.patch.object(ProjectMapper, 'verwijder_gebruiker_uit_project', return_value="")
    # testfunctie, deze later vervangen door echte functie
    def test_verwijder_gebruiker_uit_project_calls_correct_method(self, mock_verwijder_gebruiker_uit_project):
        self.project_controller.verwijder_gebruiker_uit_project(self.test_id, self.test_id, self.test_token)
        mock_verwijder_gebruiker_uit_project.assert_called()
from unittest import TestCase, mock

from app.routers.gebruiker.gebruiker_controller import GebruikerController
from app.routers.gebruiker.gebruiker_models import GebruikerResponseModel
from app.routers.gebruiker.gebruiker_repository import GebruikerMapper


class TestGebruikerController(TestCase):

    def setUp(self):
        self.gebruiker_controller = GebruikerController()
        self.gebruiker_model = GebruikerResponseModel()

    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[])
    @mock.patch.object(GebruikerMapper, 'add_user', return_value=[])
    def test_create_gebruiker_calls_controller(self, mock_create_gebruiker, mock_get_gebruikers):
        self.gebruiker_controller.create_gebruiker(self.gebruiker_model)
        mock_create_gebruiker.assert_called_with(self.gebruiker_model)

    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[])
    def test_get_gebruiker_calls_controller(self, mock_get_gebruikers):
        self.gebruiker_controller.get_gebruikers(1)
        mock_get_gebruikers.assert_called_with(1)

    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[])
    def test_get_gebruikers_calls_controller(self, mock_get_gebruikers):
        self.gebruiker_controller.get_gebruikers()
        mock_get_gebruikers.assert_called_with(None)

    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[])
    @mock.patch.object(GebruikerMapper, 'update_user', return_value=[])
    def test_update_gebruiker_calls_controller(self, mock_update_gebruiker, mock_get_gebruikers):
        self.gebruiker_controller.update_gebruiker(self.gebruiker_model)
        mock_update_gebruiker.assert_called_with(self.gebruiker_model)

    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[])
    @mock.patch.object(GebruikerMapper, 'delete_user', return_value=[])
    def test_update_gebruiker_calls_controller(self, mock_delete_gebruiker, mock_get_gebruikers):
        self.gebruiker_controller.delete_gebruiker(1)
        mock_delete_gebruiker.assert_called_with(1)

    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[])
    @mock.patch.object(GebruikerMapper, 'is_wachtwoord_tijdelijk', return_value=[])
    def test_is_wachtwoord_tijdelijk_calls_controller(self, mock_tijdeijk_wachtwoord, mock_get_gebruikers):
        self.gebruiker_controller.is_wachtwoord_tijdelijk('Daniel')
        mock_tijdeijk_wachtwoord.assert_called_with('Daniel')

    @mock.patch.object(GebruikerMapper, 'update_wachtwoord', return_value=None)
    def test_update_wachtwoord_calls_update_wachtwoord(self, mock_update_wachtwoord):
        # Act
        self.gebruiker_controller.update_wachtwoord(self.gebruiker_model)

        # Assert
        mock_update_wachtwoord.assert_called()

    @mock.patch.object(GebruikerMapper, 'check_is_beheerder', return_value=True)
    def test_check_is_beheerder_calls_check_is_beheerder(self, mock_check_is_beheerder):
        # Act
        self.gebruiker_controller.check_is_beheerder("test")

        # Assert
        mock_check_is_beheerder.assert_called()

    @mock.patch.object(GebruikerMapper, 'check_is_beheerder', return_value=True)
    def test_check_is_beheerder_returns_True(self, mock_check_is_beheerder):
        # Act
        result = self.gebruiker_controller.check_is_beheerder("test")

        # Assert
        assert result == True

    @mock.patch.object(GebruikerMapper, 'check_is_beheerder', return_value=False)
    def test_check_is_beheerder_returns_False(self, mock_check_is_beheerder):
        # Act
        result = self.gebruiker_controller.check_is_beheerder("test")

        # Assert
        assert result == False

    @mock.patch.object(GebruikerMapper, 'get_rollen', return_value=[])
    def test_get_rollen_calls_get_rollen(self, mock_get_rollen):
        # Act
        self.gebruiker_controller.get_rollen()

        # Assert
        mock_get_rollen.assert_called()

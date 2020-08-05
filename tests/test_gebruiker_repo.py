from unittest import TestCase, mock
from urllib.request import DataHandler

import mysql.connector

from app.routers.gebruiker.gebruiker_models import GebruikerResponseModel, RolResponseModel
from app.routers.gebruiker.gebruiker_repository import GebruikerMapper, GebruikerJSONParser
from app.routers.overige.overige_repository import DataMapper


class TestGebruikerRepo(TestCase):
    mapper = GebruikerMapper()

    return_object = GebruikerResponseModel()
    return_object.id = 1
    return_object.gebruikersnaam = "gebruikersnaam"
    return_object.wachtwoord = "wachtwoord"
    return_object.rol = 1
    return_object.tijdelijk_wachtwoord = 0

    return_list = [return_object, return_object]

    """test_db_connection test of de db de connector aanroept"""

    @mock.patch.object(mysql.connector, 'connect', return_value=[])
    def test_db_connection(self, mock_connect):
        self.mapper._db_connection()

        mock_connect.assert_called()

    """test_get_gebruikers_returns_lijst test of 'get gebruikers' een lijst returnt"""

    @mock.patch.object(GebruikerJSONParser, 'get_gebruikers', return_value=return_object)
    def test_get_gebruikers_returns_lijst(self, mock_parser):
        result = self.mapper.get_gebruikers(1)

        assert result.gebruikersnaam == self.return_object.gebruikersnaam

    """test_add_user_calls_mapper test of 'add_user' de mapper aanroept"""

    @mock.patch.object(GebruikerMapper, '_data_handler', return_value=[])
    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[])
    def test_add_user_calls_mapper(self, mock_get_gebruikers, mock_handler):
        gebruiker = GebruikerResponseModel()
        gebruiker.gebruikersnaam = "Gebruiker"
        gebruiker.tijdelijk_wachtwoord = 1
        gebruiker.rol = 1
        gebruiker.wachtwoord = "changeme"

        self.mapper.add_user(gebruiker)

        mock_handler.assert_called_with(
            "INSERT INTO gebruiker (gebruikersnaam, wachtwoord, rol, tijdelijk_wachtwoord) VALUES " \
            "(%s, %s, %s, %s)",
            (gebruiker.gebruikersnaam, gebruiker.wachtwoord, gebruiker.rol, gebruiker.tijdelijk_wachtwoord), False)

    """test_update_user_calls_handler test of de update functie de handler aanroept"""

    @mock.patch.object(GebruikerMapper, '_data_handler', return_value=[])
    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[])
    def test_update_user_calls_handler(self, mock_get_gebruikers, mock_handler):
        gebruiker = GebruikerResponseModel()
        gebruiker.id = 1
        gebruiker.gebruikersnaam = "Gebruiker"
        gebruiker.tijdelijk_wachtwoord = 1
        gebruiker.rol = 1
        gebruiker.wachtwoord = "changeme"

        self.mapper.update_user(gebruiker)

        mock_handler.assert_called_with(
            "UPDATE gebruiker SET gebruikersnaam = %s, wachtwoord = %s, rol = %s, tijdelijk_wachtwoord = %s WHERE id = %s",
            (gebruiker.gebruikersnaam, gebruiker.wachtwoord, gebruiker.rol, gebruiker.tijdelijk_wachtwoord,
             gebruiker.id), False)

    """test_delete_user_returns_list_of_users test of het verwijderen van een gebruiker een lijst met gebruikers 
    teruggeeft """

    @mock.patch.object(GebruikerMapper, '_data_handler', return_value=[])
    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=return_list)
    def test_delete_user_returns_list_of_users(self, get_mock, mock_handler):
        result = self.mapper.delete_user(1)

        assert result[0].gebruikersnaam == self.return_list[0].gebruikersnaam

    @mock.patch.object(GebruikerMapper, '_data_handler', return_value=[])
    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=return_list)
    def test_get_tijdelijk_wachtwoord_returns_int(self, get_mock, mock_handler):
        result = self.mapper.is_wachtwoord_tijdelijk(self.return_object.gebruikersnaam)

        assert result == self.return_list[0].tijdelijk_wachtwoord

    @mock.patch.object(GebruikerMapper, '_data_handler', return_value=[])
    def test_update_wachtwoord_calls__data_handler(self, mock__data_handler):
        # Act
        self.mapper.update_wachtwoord(self.return_object)

        # Assert
        mock__data_handler.assert_called()

    @mock.patch.object(GebruikerMapper, '_data_handler', return_value=[(1,)])
    def test_check_is_beheerder_calls__data_handler(self, mock__data_handler):
        # Act
        self.mapper.check_is_beheerder("test")

        # Assert
        mock__data_handler.assert_called()

    @mock.patch.object(GebruikerMapper, '_data_handler', return_value=[(1,)])
    def test_check_is_beheerder_returns_True(self, mock__data_handler):
        # Act
        result = self.mapper.check_is_beheerder("test")

        # Assert
        assert result == True

    @mock.patch.object(GebruikerMapper, '_data_handler', return_value=[(0,)])
    def test_check_is_beheerder_returns_False(self, mock__data_handler):
        # Act
        result = self.mapper.check_is_beheerder("test")

        # Assert
        assert result == False

    @mock.patch.object(GebruikerMapper, '_data_handler', return_value=[(1, 'stuff')])
    def test_get_rollen_returns_array_with_the_correct_length(self, mock__data_handler):
        # Arrange
        expected_length = 1

        # Act
        result = self.mapper.get_rollen()

        # Assert
        mock__data_handler.assert_called()
        assert len(result) == expected_length

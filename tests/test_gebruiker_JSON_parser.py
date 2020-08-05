from unittest import TestCase, mock

from app.routers.gebruiker.gebruiker_models import GebruikerResponseModel
from app.routers.gebruiker.gebruiker_repository import GebruikerJSONParser
from builtins import type as BuiltInType


class TestGebruikerJSONParser(TestCase):
    return_object = GebruikerResponseModel()
    return_object.id = 1
    return_object.gebruikersnaam = "gebruikersnaam"
    return_object.wachtwoord = "wachtwoord"
    return_object.rol = 1
    return_object.tijdelijk_wachtwoord = 0

    return_object2 = GebruikerResponseModel()
    return_object2.id = 2
    return_object2.gebruikersnaam = "gebruikersnaam"
    return_object2.wachtwoord = "wachtwoord"
    return_object2.rol = 1
    return_object2.tijdelijk_wachtwoord = 0

    return_list = [return_object, return_object2]

    """test_get_gebruikers_returns_empty_list test of het aanroepen van get gebruikers een lege lijst teruggeeft"""

    @mock.patch.object(GebruikerJSONParser, '_data_handler', return_value=[])
    def test_get_gebruikers_returns_empty_list(self, mocked_handler):
        parser = GebruikerJSONParser()

        result = parser.get_gebruikers()

        assert result == []

    """test_get_gebruikers_gets_list_of_gebruikers test of get gebruikers een lijst met gebruikers teruggeeft"""

    @mock.patch.object(GebruikerJSONParser, '_data_handler', return_value=return_list)
    def test_get_gebruikers_gets_list_of_gebruikers(self, mocked_handler):
        parser = GebruikerJSONParser()

        result = parser.get_gebruikers()

        assert result[0].gebruikersnaam == self.return_object2.gebruikersnaam

    """test_get_gebruiker_returns_one_gebruiker test of get gebruikers een enkele gebruiker teruggeeft"""

    @mock.patch.object(GebruikerJSONParser, '_data_handler', return_value=return_list)
    def test_get_gebruiker_returns_one_gebruiker(self, mocked_handler):
        parser = GebruikerJSONParser()

        result = parser.get_gebruikers(1)

        assert result.gebruikersnaam == self.return_object.gebruikersnaam

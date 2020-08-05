from unittest import TestCase, mock

from fastapi import HTTPException

from app.routers.gebruiker.gebruiker_controller import GebruikerController
from app.routers.overige.overige_authentication_service import AuthenticationService
from app.routers.gebruiker.gebruiker_models import TokenModel, GebruikerResponseModel
from app.routers.gebruiker.gebruiker_repository import GebruikerMapper


class TestAuthenticationService(TestCase):
    auth = AuthenticationService()

    token_model = TokenModel(token='test', verloop=-1)

    """test_add_token_adds_token test of er een token toegevoegd kan worden aan de cache"""

    def test_add_token_adds_token(self):

        self.auth._add_token(self.token_model)

        includes = self.auth.token_cache.__contains__(self.token_model)

        self.auth._delete_token(self.token_model)

        assert includes

    """test_delete_token_deletes_token test of het verwijderen van een token uit de cache werkt"""

    def test_delete_token_deletes_token(self):
        self.auth._add_token(self.token_model)
        self.auth._delete_token(self.token_model)

        includes = self.auth.token_cache.__contains__(self.token_model)

        assert not includes

    """test_check_expirations_removes_token checkt of _check_expirations de verlopen tokens verwijdert """

    def test_check_expirations_removes_token(self):
        self.auth._check_expirations()

        includes = self.auth.token_cache.__contains__(self.token_model)

        assert not includes

    """test_check_expirations_calls_remove_token test of de methode de _delete_token methode aanroept"""

    @mock.patch.object(AuthenticationService, '_delete_token', return_value=[])
    def test_check_expirations_calls_remove_token(self, mock_delete_token):
        self.auth._add_token(self.token_model)

        self.auth._check_expirations()

        mock_delete_token.assert_called_with(self.token_model)

    """test_check_wachtwoord_returns_false checkt of check_wachtwoord geen foutieve wachtwoorden doorlaat"""

    def test_check_wachtwoord_returns_false(self):
        foutieve_hash = self.auth.hash_wachtwoord('foutieve_hash')

        assert not self.auth._check_wachtwoord('string', foutieve_hash)

    """test_check_wachtwoord_returns_true checkt of een juist wachtwoord door de hash komt"""

    def test_check_wachtwoord_returns_true(self):
        goede_hash = self.auth.hash_wachtwoord('string')

        assert self.auth._check_wachtwoord('string', goede_hash)

    """test_generate_token_returns_token test of er een token wordt gegenereerd door generate_token"""

    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[
        GebruikerResponseModel(id=1, gebruikersnaam='Daniel', wachtwoord='wachtwoord', rol=0, tijdelijk_wachtwoord=0)])
    def test_generate_token_returns_token(self, mocked_gebruikers):
        gebruikersnaam = 'Daniel'

        token = self.auth.generate_token(gebruikersnaam)

        assert self.auth.check_if_token_in_cache(token.token)

    """test_check_if_token_in_cache_returns_true checkt of de token gevonden kan worden in de cache"""

    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[
        GebruikerResponseModel(id=1, gebruikersnaam='Daniel', wachtwoord='wachtwoord', rol=0, tijdelijk_wachtwoord=0)])
    def test_check_if_token_in_cache_returns_true(self, mocked_gebruikers):
        gebruikersnaam = "Daniel"

        token = self.auth.generate_token(gebruikersnaam)

        assert self.auth.check_if_token_in_cache(token.token)

    """test_check_if_token_in_cache_returns_false checkt of een onjuist token niet kan worden gevonden in de cache"""

    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[
        GebruikerResponseModel(id=1, gebruikersnaam='Daniel', wachtwoord='wachtwoord', rol=0, tijdelijk_wachtwoord=0)])
    def test_check_if_token_in_cache_returns_false(self, mocked_gebruiker):
        gebruikersnaam = "Daniel"

        self.auth.generate_token(gebruikersnaam)

        token = self.auth.hash_wachtwoord('fake_token')

        assert not self.auth.check_if_token_in_cache(token)

    """test_can_user_access_returns_true test of de gebruiker gevalideerd kan worden vanuit de cache"""

    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[
        GebruikerResponseModel(id=1, gebruikersnaam='Daniel', wachtwoord='wachtwoord', rol=0, tijdelijk_wachtwoord=0)])
    def test_can_user_access_returns_true(self, mocked_gebruikers):
        token = self.auth.generate_token('Daniel')

        assert self.auth.can_user_access(token.token)

    """test_can_user_access_throws_exception test of de functie een exception teruggeeft als de token niet bestaat"""

    def test_can_user_access_throws_exception(self):
        self.assertRaises(HTTPException, self.auth.can_user_access, 'no_token')

    """test_authticate_throws_exception_if_no_users test of de functie een exceptie geeft als er geen gebruikers in 
    de database staan """

    @mock.patch.object(GebruikerController, 'get_gebruikers', return_value=None)
    def test_authticate_throws_exception_if_no_users(self, mocked_result):
        gebruikersnaam = "Daniel"
        wachtwoord = 'onjuist_wachtwoord'

        self.assertRaises(HTTPException, self.auth.authenticate_user, gebruikersnaam, wachtwoord)

    """test_check_if_authenticate_returns_true checkt of een gebruiker in kan loggen loggen met juiste gegevens"""

    @mock.patch.object(GebruikerController, "get_gebruikers", return_value=[
        GebruikerResponseModel(id=1, gebruikersnaam='test',
                               wachtwoord='$2y$12$qjdhqWU1ORp.7GUnkqjT4.g0Nzh//GhvyM6afMsGAj9vt.Rh.zSQC', rol=0,
                               tijdelijk_wachtwoord=0)]
                       )
    def test_check_if_authenticate_returns_true(self, mocked_gebruiker_response):
        gebruikersnaam = 'test'
        wachtwoord = 'wachtwoord'

        assert self.auth.authenticate_user(gebruikersnaam, wachtwoord)

    """test_check_if_user_has_token_returns_exception checkt of de functie een exception teruggeeft als het 
    wachtwoord onjuist is """

    @mock.patch.object(GebruikerController, "get_gebruikers", return_value=[
        GebruikerResponseModel(id=1, gebruikersnaam='test',
                               wachtwoord='$2y$12$qjdhqWU1ORp.7GUnkqjT4.g0Nzh//GhvyM6afMsGAj9vt.Rh.zSQC', rol=0,
                               tijdelijk_wachtwoord=0)]
                       )
    def test_check_if_user_has_token_returns_exception(self, mocked_gebruiker_response):
        gebruikersnaam = "test"
        wachtwoord = 'onjuist_wachtwoord'

        self.assertRaises(HTTPException, self.auth.authenticate_user, gebruikersnaam, wachtwoord)

    """test_hash_wachtwoord_returns_hashed_wachtwoord test of er een wachtwoord gehasht kan worden"""

    def test_hash_wachtwoord_returns_hashed_wachtwoord(self):
        wachtwoord = 'test'

        result = self.auth.hash_wachtwoord(wachtwoord)

        assert self.auth._check_wachtwoord(wachtwoord, result)

    @mock.patch.object(auth, 'get_user_by_token', return_value="naam")
    @mock.patch.object(GebruikerController, 'check_is_beheerder', return_value=True)
    def test_check_of_user_is_beheerder_calls_check_is_beheerder(self, mocked_check_of_user_is_beheerder, mocked_get_user_by_token):
        self.auth.check_of_user_is_beheerder("token")
        mocked_check_of_user_is_beheerder.assert_called_with("naam")

    @mock.patch.object(auth, 'get_user_by_token', return_value="naam")
    @mock.patch.object(GebruikerController, 'check_is_beheerder', return_value=True)
    def test_check_of_user_is_beheerder_calls_check_is_beheerder(self, mocked_check_of_user_is_beheerder, mocked_get_user_by_token):
        self.auth.check_of_user_is_beheerder("token")
        mocked_get_user_by_token.assert_called_with("token")

    @mock.patch.object(auth, 'get_user_by_token', return_value="naam")
    @mock.patch.object(GebruikerController, 'check_is_beheerder', return_value=True)
    def test_check_of_user_is_beheerder_returns_True(self, mocked_check_of_user_is_beheerder, mocked_get_user_by_token):
        result = self.auth.check_of_user_is_beheerder("token")

        assert result == True

    @mock.patch.object(auth, 'get_user_by_token', return_value="naam")
    @mock.patch.object(GebruikerController, 'check_is_beheerder', return_value=False)
    def test_check_of_user_is_beheerder_returns_False(self, mocked_check_of_user_is_beheerder, mocked_get_user_by_token):
        result = self.auth.check_of_user_is_beheerder("token")

        assert result == False
from unittest import TestCase, mock

from fastapi import HTTPException
from starlette.testclient import TestClient

from app.routers.overige.overige_authentication_service import AuthenticationService
from app.routers.gebruiker.gebruiker_models import GebruikerResponseModel
from app.routers.gebruiker.gebruiker_repository import GebruikerMapper
from app.routers.gebruiker.gebruiker_view import app
from app.routers.overige.overige_repository import DataMapper
from app.routers.gebruiker.gebruiker_controller import GebruikerController


class TestGebruikerView(TestCase):
    """test_get_gebruikers test of get_gebruikers de correcte status code teruggeeft"""

    def setUp(self):
        self.sut = TestClient(app)
        self.gebruiker = GebruikerResponseModel()
        self.token = "1234-1234-1234-1234"

    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[])
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    def test_get_gebruikers(self, mocked_auth, mocked_get_gebruikers):
        response = self.sut.get("/?token=" + self.token)
        assert response.status_code == 200

    """test_get_gebruikers_json test of get_gebruikers een json lijst teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[])
    def test_get_gebruikers_json(self, mocked_get_gebruikers, mocked_auth):
        response = self.sut.get("/?token=" + self.token)
        assert response.json() == []

    """test_post_gebruiker test of post_gebruiker de correcte status code teruggeeft"""

    @mock.patch.object(GebruikerMapper, 'add_user', return_value=[
        GebruikerResponseModel(id=1, gebruikersnaam='Daniel', wachtwoord='wachtwoord', rol=0, tijdelijk_wachtwoord=0)])
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(AuthenticationService, 'check_of_user_is_beheerder', return_value=True)
    def test_post_gebruiker(self, mocked_auth, mocked_add_user, mocked_check_of_user_is_beheerder):
        response = self.sut.post("/?token=" + self.token, json={
            'id': 1,
            'gebruikersnaam': 'nieuwe_gebruiker',
            'wachtwoord': 'wachtwoord',
            'rol': 0,
            'tijdelijk_wachtwoord': 0
        })
        assert response.status_code == 201

    """test_post_gebruiker_json test of post_gebruiker een json lijst teruggeeft"""

    @mock.patch.object(GebruikerMapper, 'add_user', return_value=[
        GebruikerResponseModel(id=1, gebruikersnaam='Daniel', wachtwoord='wachtwoord', rol=0, tijdelijk_wachtwoord=0)])
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(AuthenticationService, 'check_of_user_is_beheerder', return_value=True)
    def test_post_gebruiker_json(self, mocked_auth, mocked_add_user, mocked_check_of_user_is_beheerder):
        response = self.sut.post("/?token=" + self.token, json={
            "id": "1",
        })
        assert response.status_code == 201

    """test_update_gebruiker test of update_gebruiker de correcte status code teruggeeft"""

    @mock.patch.object(GebruikerMapper, 'update_user', return_value=[
        GebruikerResponseModel(id=1, gebruikersnaam='Daniel', wachtwoord='wachtwoord', rol=0, tijdelijk_wachtwoord=0)])
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(AuthenticationService, 'check_of_user_is_beheerder', return_value=True)
    def test_update_gebruiker(self, mocked_auth, mocked_update_user, mocked_check_of_user_is_beheerder):
        response = self.sut.put("/?token=" + self.token, json={
            "id": "1",
        })
        assert response.status_code == 200

    """test_update_gebruiker tes of update_gebruiker een json lijst teruggeeft"""

    @mock.patch.object(GebruikerMapper, 'update_user', return_value=[
        GebruikerResponseModel(id=1, gebruikersnaam='Daniel', wachtwoord='wachtwoord', rol=0, tijdelijk_wachtwoord=0)])
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(AuthenticationService, 'check_of_user_is_beheerder', return_value=True)
    def test_update_gebruiker_json(self, mocked_auth, mocked_update_user, mocked_check_of_user_is_beheerder):
        response = self.sut.put("/?token=" + self.token, json={
            "id": "1",
        })
        assert response.status_code == 200

    """test_delete_gebruiker test of delete_gebruiker de juiste status code teruggeeft"""

    @mock.patch.object(DataMapper, '_stored_procedure', return_value="return_value")
    @mock.patch.object(GebruikerMapper, 'delete_user', return_value=[])
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(AuthenticationService, 'check_of_user_is_beheerder', return_value=True)
    def test_delete_gebruiker(self, mocked_auth, mocked_gebruikers, mocked_data_mapper,
                              mocked_check_of_user_is_beheerder):
        response = self.sut.delete("/1/?token=" + self.token)
        assert response.status_code == 200

    """test_delete_gebruiker_json test od delete_gebruiker een json lijst teruggeeft"""

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(AuthenticationService, 'check_of_user_is_beheerder', return_value=True)
    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[])
    @mock.patch.object(GebruikerMapper, 'delete_user', return_value=[])
    def test_delete_gebruiker_json(self, mocked_delete, mocked_gebruikers, mocked_auth,
                                   mocked_check_of_user_is_beheerder):
        response = self.sut.delete("/1/?token=" + self.token)
        assert response.json() == []

    """Test of login() een status code 200 terug geeft"""

    @mock.patch.object(GebruikerMapper, 'get_gebruikers', return_value=[
        GebruikerResponseModel(id=1, gebruikersnaam='Daniel',
                               wachtwoord='$2y$12$qjdhqWU1ORp.7GUnkqjT4.g0Nzh//GhvyM6afMsGAj9vt.Rh.zSQC', rol=0,
                               tijdelijk_wachtwoord=0)])
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    def test_login_geeft_een_200_status_code(self, mocked_auth, mocked_get_gebruikers):
        response = self.sut.post("/login", json={'id': 1,
                                                 'gebruikersnaam': 'Daniel',
                                                 'wachtwoord': 'wachtwoord',
                                                 'rol': 0,
                                                 'tijdelijk_wachtwoord': 0})
        assert response.status_code == 200

    """Test of login() de juiste token terug stuurt"""

    @mock.patch.object(AuthenticationService, 'authenticate_user', return_value=True)
    @mock.patch.object(AuthenticationService, 'generate_token', return_value='1234-1234-1234-1234')
    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    def test_login_geeft_een_token(self, mocked_access, mocked_token, mocked_auth):
        response = self.sut.post("/login", json={
            'id': 1,
            'gebruikersnaam': 'Daniel',
            'wachtwoord': 'wachtwoord',
            'rol': 0,
            'tijdelijk_wachtwoord': 0
        })
        print(response)
        assert response.json() == self.token

    """Test of verify() de juiste boolean terug stuurt"""

    @mock.patch.object(AuthenticationService, 'check_if_token_in_cache', return_value=True)
    def test_verify_retourneerd_true(self, mocked_auth):
        response = self.sut.get("/verify?token=" + self.token)
        assert response

    """Test of update_wachtwoord() check_if_token_in_cache() aanroept"""

    @mock.patch.object(GebruikerController, 'update_wachtwoord', return_value=None)
    @mock.patch.object(AuthenticationService, 'hash_wachtwoord', return_value="string")
    @mock.patch.object(AuthenticationService, 'get_user_by_token', return_value="string")
    @mock.patch.object(AuthenticationService, 'check_if_token_in_cache', return_value=True)
    def test_update_wachtwoord_called_auth_check_if_token_in_cache(self, mock_check_if_token_in_cache,
                                                                   mock_get_user_by_token, mock_hash_password,
                                                                   mock_update_wachtwoord):
        # Arrange

        # Act
        self.sut.put("/update_password?token=" + self.token, self.gebruiker.json())

        # Assert
        mock_check_if_token_in_cache.assert_called()

    """Test of update_wachtwoord() get_user_by_token() aanroept"""

    @mock.patch.object(GebruikerController, 'update_wachtwoord', return_value=None)
    @mock.patch.object(AuthenticationService, 'hash_wachtwoord', return_value="string")
    @mock.patch.object(AuthenticationService, 'get_user_by_token', return_value="string")
    @mock.patch.object(AuthenticationService, 'check_if_token_in_cache', return_value=True)
    def test_update_wachtwoord_called_auth_get_user_by_token(self, mock_check_if_token_in_cache,
                                                             mock_get_user_by_token, mock_hash_password,
                                                             mock_update_wachtwoord):
        # Arrange

        # Act
        self.sut.put("/update_password?token=" + self.token, self.gebruiker.json())

        # Assert
        mock_get_user_by_token.assert_called()

    """Test of update_wachtwoord() hash_wachtwoord aanroept"""

    @mock.patch.object(GebruikerController, 'update_wachtwoord', return_value=None)
    @mock.patch.object(AuthenticationService, 'hash_wachtwoord', return_value="string")
    @mock.patch.object(AuthenticationService, 'get_user_by_token', return_value="string")
    @mock.patch.object(AuthenticationService, 'check_if_token_in_cache', return_value=True)
    def test_update_wachtwoord_called_auth_hash_password(self, mock_check_if_token_in_cache,
                                                         mock_get_user_by_token, mock_hash_password,
                                                         mock_update_wachtwoord):
        # Arrange

        # Act
        self.sut.put("/update_password?token=" + self.token, self.gebruiker.json())

        # Assert
        mock_hash_password.assert_called()

    """Test of update_wachtwoord() update_wachtwoord() aanroept"""

    @mock.patch.object(GebruikerController, 'update_wachtwoord', return_value=None)
    @mock.patch.object(AuthenticationService, 'hash_wachtwoord', return_value="string")
    @mock.patch.object(AuthenticationService, 'get_user_by_token', return_value="string")
    @mock.patch.object(AuthenticationService, 'check_if_token_in_cache', return_value=True)
    def test_update_wachtwoord_called_controller_update_password(self, mock_check_if_token_in_cache,
                                                                 mock_get_user_by_token, mock_hash_password,
                                                                 mock_update_wachtwoord):
        # Arrange

        # Act
        self.sut.put("/update_password?token=" + self.token, self.gebruiker.json())

        # Assert
        mock_update_wachtwoord.assert_called()

    @mock.patch.object(GebruikerController, 'update_wachtwoord', return_value=None)
    @mock.patch.object(AuthenticationService, 'hash_wachtwoord', return_value="string")
    @mock.patch.object(AuthenticationService, 'get_user_by_token', return_value="string")
    @mock.patch.object(AuthenticationService, 'check_if_token_in_cache', return_value=False)
    def test_update_wachtwoord_raises_HTTPException(self, mock_check_if_token_in_cache,
                                                    mock_get_user_by_token, mock_hash_password,
                                                    mock_update_wachtwoord):
        # Arrange

        # Act
        try:
            self.sut.put("/update_password?token=" + self.token, self.gebruiker.json())
        # Assert
        except HTTPException as err:
            assert err.detail == 'Uw token is ongeldig of verlopen'

    @mock.patch.object(AuthenticationService, 'check_of_user_is_beheerder', return_value=True)
    def test_is_beheerder_calls_correct_method(self, mock_check_of_user_is_beheerder):
        self.sut.get('/is_beheerder?token=' + self.token)
        mock_check_of_user_is_beheerder.assert_called_with(self.token)

    @mock.patch.object(AuthenticationService, 'check_of_user_is_beheerder', return_value=True)
    @mock.patch.object(GebruikerController, 'get_rollen', return_value=[])
    def test_get_rollen_calls_correct_methods_when_user_is_beheerder(self, mock_get_rollen,
                                                                     mock_check_of_user_is_beheerder):
        # Act
        self.sut.get('/rollen?token=' + self.token)

        # Assert
        mock_get_rollen.assert_called()
        mock_check_of_user_is_beheerder.assert_called()

    @mock.patch.object(AuthenticationService, 'check_of_user_is_beheerder', return_value=False)
    @mock.patch.object(GebruikerController, 'get_rollen', return_value=[])
    def test_get_rollen_thows_exception_when_not_beheerder(self, mock_get_rollen, mock_check_of_user_is_beheerder):
        # Act
        try:
            self.sut.get("/rollen?token=" + self.token)
        # Assert
        except HTTPException as err:
            assert err.detail == 'U bent geen beheerder'

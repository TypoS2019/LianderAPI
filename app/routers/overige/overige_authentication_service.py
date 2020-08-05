import uuid
from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from app.routers.gebruiker.gebruiker_controller import GebruikerController
from app.routers.gebruiker.gebruiker_models import TokenModel, TokenResponseModel


class AuthenticationService:
    """Unauthorized Exception is de exceptie die gegeven wordt als de gebruiker foutieve gegevens invult"""
    unauthorized_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Gebruikersnaam of wachtwoord is onjuist",
    )

    """Forbidden Exception is de exceptie die gegeven wordt als de gebruiker een pagina probeert te laden terwijl hij 
    niet is ingelogd. """
    forbidden_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="Voor toegang tot deze pagina is inloggen vereist",
    )

    """Token_Cache is de cache die de tokens bijhoudt."""
    token_cache = [
        TokenModel(token='1234-1234-1234-1234', gebruikersnaam="admin",
                   verloop=float(datetime.timestamp(datetime.now() + timedelta(weeks=5200))))
        # Er staat één token in de cache, om te testen. Deze token moet verwijderd worden als de applicatie gaat worden
        # gebruikt in verband met de veiligheid
    ]

    controller = GebruikerController()

    """_add_token voegt een token toe aan de cache"""

    def _add_token(self, model: TokenModel):
        self.token_cache.append(model)

    """_delete_token verwijdert een token uit de cache"""

    def _delete_token(self, model: TokenModel):
        self.token_cache.remove(model)

    """_check_expirations kijkt voor de hele cache of de tokens nog geldig zijn"""

    def _check_expirations(self):
        for token in self.token_cache:
            timestamp = datetime.timestamp(datetime.now())
            if token.verloop <= timestamp:  # Als de token in de cache ouder is dan de huidige tijd
                self._delete_token(token)  # Wordt de token uit de cache verwijderd

    """_check_wachtwoord vergelijkt het 'kale' wachtwoord met de gehashte variant"""

    def _check_wachtwoord(self, unhashed_wachtwoord, hashed_wachtwoord):
        unhashed_wachtwoord = unhashed_wachtwoord.encode('utf-8')
        if type(hashed_wachtwoord) != bytes:
            hashed_wachtwoord = hashed_wachtwoord.encode('utf-8')
        if bcrypt.checkpw(unhashed_wachtwoord, hashed_wachtwoord):
            return True
        return False

    """generate_token genereert een token die aan de gebruikersnaam is gekoppeld"""

    def generate_token(self, username: str, verloop: int = 30):
        self._check_expirations()  # De functie kijkt eerst of er outdated tokens in de cache staan en verwijdert
        # deze waar nodig
        token = str(uuid.uuid4())  # Genereer een random UUID als token

        expire_datetime_raw = datetime.now() + timedelta(
            minutes=verloop)  # Er wordt een datetime object gemaakt van de tijd waarop de token zal verlopen
        expire_datetime = float(datetime.timestamp(
            expire_datetime_raw))  # Hiervan wordt een timestamp gemaakt die naar een float wordt omgezet voor in het
        # model

        token_model = TokenModel(token=token, gebruikersnaam=username,
                                 verloop=expire_datetime)  # Hiervan wordt een TokenModel gemaakt

        self.token_cache.append(token_model)  # En deze wordt in de cache gezet

        tijdelijk_wachtwoord = self.controller.is_wachtwoord_tijdelijk(username)

        return_token = TokenResponseModel(token=token, tijdelijk_wachtwoord=int(tijdelijk_wachtwoord))

        return return_token  # Het token zelf wordt teruggegeven

    """check_if_user_has_token checkt of er een token in de cache staat die bij de gespecificeerde gebruiker hoort"""

    def check_if_token_in_cache(self, token):
        self._check_expirations()
        for token_item in self.token_cache:  # Voor iedere token in de cache
            if token_item.token == token:  # Kijken we of deze overeen komt met de token in de cache
                expire_datetime_raw = datetime.now() + timedelta(
                    minutes=30)  # Er wordt een datetime object gemaakt van de tijd waarop de token zal verlopen
                expire_datetime = float(datetime.timestamp(
                    expire_datetime_raw))  # Hiervan wordt een timestamp gemaakt die naar een float wordt omgezet voor in het
                # model
                token_item.verloop = expire_datetime
                return True  # Als dat zo is dan retourneren we true

        return False  # Anders heeft de gebruiker geen token

    """can_user_access geeft 'true' terug als de gebruiker is ingelogd. Het geeft een exception als dat niet zo is"""

    def can_user_access(self, token):
        self._check_expirations()
        if self.check_if_token_in_cache(token):
            return True

        raise self.forbidden_exception

    """authenticate_user wordt gebruikt om een gebruiker in te loggen"""

    def authenticate_user(self, gebruikernaam: str, wachtwoord: str):
        self._check_expirations()
        gebruikers = self.controller.get_gebruikers()  # De methode haalt alle gebruikers uit de database

        if not gebruikers:  # Als er geen gebruikers in de database staan
            raise self.unauthorized_exception  # Is de gebruiker sowieso niet geautenticeerd
        for gebruiker in gebruikers:  # Voor iedere gebruikersnaam in de database
            if gebruiker.gebruikersnaam == gebruikernaam and self._check_wachtwoord(wachtwoord,
                                                                                    gebruiker.wachtwoord):  # Als de
                # gebruikersnaam die is meegegeven in de gebruikersnaam staat en het wachtwoord ook overeen komt
                return True  # Retourneren we 'true'

        raise self.unauthorized_exception  # In ieder ander geval geven we een exception

    """hash_wachtwoord zet een 'plain' wachtwoord om naar een hash.s"""

    def hash_wachtwoord(self, wachtwoord):
        self._check_expirations()
        wachtwoord = wachtwoord.encode('utf-8')
        return bcrypt.hashpw(wachtwoord, bcrypt.gensalt())

    def get_user_by_token(self, token):
        for token_model in self.token_cache:
            if token_model.token == token:
                return token_model.gebruikersnaam
        raise HTTPException(status_code=401, detail="Uw token is onjuist of verlopen")

    def check_of_user_is_beheerder(self, token):
        gebruikersnaam = self.get_user_by_token(token)
        return GebruikerController().check_is_beheerder(gebruikersnaam)

    def get_id_by_gebruikersnaam(self, gebruikersnaam):
        return GebruikerController().get_id_by_gebruikersnaam(gebruikersnaam)

    def can_user_access_scenario(self, token, project_id):
        gebruikersnaam = self.get_user_by_token(token)
        gebruikers_id = self.get_id_by_gebruikersnaam(gebruikersnaam)
        return GebruikerController().can_user_access_scenario(gebruikers_id, project_id)




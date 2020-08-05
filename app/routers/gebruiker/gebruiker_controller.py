import bcrypt

from app.routers.gebruiker.gebruiker_models import GebruikerResponseModel
from app.routers.gebruiker.gebruiker_repository import GebruikerMapper


class GebruikerController(object):

    def __init__(self):
        self.mapper = GebruikerMapper()

    def hash_wachtwoord(self, wachtwoord):
        wachtwoord = str(wachtwoord)
        wachtwoord = wachtwoord.encode('utf-8')
        return bcrypt.hashpw(wachtwoord, bcrypt.gensalt())

    """Onderstaande functies verwijzen de requests door naar de repository laag"""

    def create_gebruiker(self, model: GebruikerResponseModel):
        return self.mapper.add_user(model)

    def get_gebruikers(self, gebruiker_id: int = None):
        return self.mapper.get_gebruikers(gebruiker_id)

    def update_gebruiker(self, model: GebruikerResponseModel):
        return self.mapper.update_user(model)

    def delete_gebruiker(self, gebruiker_id: int):
        return self.mapper.delete_user(gebruiker_id)

    def is_wachtwoord_tijdelijk(self, gebruikersnaam: str):
        return self.mapper.is_wachtwoord_tijdelijk(gebruikersnaam)

    def update_wachtwoord(self, gebruiker: GebruikerResponseModel):
        self.mapper.update_wachtwoord(gebruiker)

    def check_is_beheerder(self, naam: str):
        return self.mapper.check_is_beheerder(naam)

    def get_rollen(self):
        return self.mapper.get_rollen()

    def get_id_by_gebruikersnaam(self, gebruikersnaam):
        return self.mapper.get_gebruiker_id_by_gebruikersnaam(gebruikersnaam)

    def can_user_access_scenario(self, gebruiker_id, project_id):
        return self.mapper.can_user_access_scenario(gebruiker_id, project_id)
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from app.routers.overige.overige_repository import DataMapper, JSONParser
from app.routers.gebruiker.gebruiker_models import GebruikerResponseModel, RolResponseModel


class GebruikerMapper(DataMapper):
    """get_gebruikers retourneert de gebruikers uit de database"""

    def get_gebruikers(self, id: int = None):
        parser = GebruikerJSONParser()

        return parser.get_gebruikers(id)

    """add_user voegt een gebruiker toe aan de database"""

    def add_user(self, model: GebruikerResponseModel):
        query = "INSERT INTO gebruiker (gebruikersnaam, wachtwoord, rol, tijdelijk_wachtwoord) VALUES " \
                "(%s, %s, %s, %s)"
        values = (model.gebruikersnaam, model.wachtwoord, model.rol, int(model.tijdelijk_wachtwoord))
        self._data_handler(query, values, False)

        self.logger.info(("Added user with name: " + str(model.gebruikersnaam)), source=self.source_name)

        return self.get_gebruikers()

    """update_user past de waardes van een bepaalde gebruiker aan in de database"""

    def update_user(self, model: GebruikerResponseModel):
        query = "UPDATE gebruiker SET gebruikersnaam = %s, wachtwoord = %s, rol = %s, tijdelijk_wachtwoord = %s WHERE id = %s"
        values = (model.gebruikersnaam, model.wachtwoord, model.rol, int(model.tijdelijk_wachtwoord), model.id)

        self._data_handler(query, values, False)

        return self.get_gebruikers()

    """delete_user verwijdert een gebruiker uit de database"""

    def delete_user(self, gebruiker_id: int):
        query = "DELETE FROM gebruiker WHERE id = %s"
        value = (gebruiker_id,)

        self._data_handler(query, value, False)

        return self.get_gebruikers()

    def is_wachtwoord_tijdelijk(self, gebruikersnaam):
        gebruikers = self.get_gebruikers()

        for gebruiker in gebruikers:
            if gebruiker.gebruikersnaam == gebruikersnaam:
                return gebruiker.tijdelijk_wachtwoord
        return HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Gebruikersnaam of wachtwoord is onjuist",
        )

    """Update het wachtwoord bij de gebruiker en zet de kolom tijdelijk_wachtwoord op 0"""

    def update_wachtwoord(self, gebruiker: GebruikerResponseModel):
        query = "UPDATE gebruiker SET wachtwoord = %s, tijdelijk_wachtwoord = 0 WHERE gebruikersnaam = %s"
        values = (gebruiker.wachtwoord, gebruiker.gebruikersnaam,)

        self._data_handler(query, values, False)

    """Vraagt aan de database of de meegestuurde gebruikersnaam een beheerder is"""

    def check_is_beheerder(self, naam):
        query = "SELECT CASE WHEN gr.rol = 'Beheerder' THEN True ELSE False END AS beheerder " + \
                "FROM gebruiker g JOIN gebruiker_rollen gr ON g.rol = gr.id WHERE g.gebruikersnaam = %s"
        value = (naam,)
        result = self._data_handler(query, value, True)
        for row in result:
            is_beheerder = row[0]

        if is_beheerder == 1:
            return True
        else:
            return False

    def get_rollen(self):
        query = "SELECT * FROM gebruiker_rollen"
        value = None
        result = self._data_handler(query, value, True)

        rollen = []

        for row in result:
            model = RolResponseModel()
            model.id = row[0]
            model.rol = row[1]
            rollen.append(model)

        return rollen
    def get_gebruiker_id_by_gebruikersnaam(self, gebruikersnaam):
        query = "SELECT id FROM gebruiker WHERE gebruikersnaam = %s"
        result = self._data_handler(query, (gebruikersnaam,), True)

        if result:
            for result_item in result:
                return result_item[0]
        else:
            return None

    def can_user_access_scenario(self, gebruiker_id, project_id):
        query = "SELECT * FROM "


class GebruikerJSONParser(JSONParser):
    """get_gebruikers handelt de vraag naar de users (een of meerdere) af met de database"""

    def get_gebruikers(self, id: int = None):
        query = None
        value = None
        if id is None:  # als er geen id is meegegeven
            query = "SELECT * FROM gebruiker"  # selecteren we alles uit de database
        else:
            query = "SELECT * FROM gebruiker WHERE id = %s"  # anders geven we dat id mee
            value = (id,)

        result = self._data_handler(query, value, True)

        gebruiker_lijst = []
        for row in result:  # voor iedere gebruiker die meegegeven wordt
            gebruiker = GebruikerResponseModel()  # maken we een nieuw model aan
            if type(row) == GebruikerResponseModel:
                gebruiker.id = row.id
                gebruiker.gebruikersnaam = row.gebruikersnaam
                gebruiker.wachtwoord = row.wachtwoord
                gebruiker.rol = row.rol
                gebruiker.tijdelijk_wachtwoord = row.tijdelijk_wachtwoord
            if type(row) == tuple:
                gebruiker.id = row[0]
                gebruiker.gebruikersnaam = row[1]
                gebruiker.wachtwoord = row[2]
                gebruiker.rol = row[3]
                gebruiker.tijdelijk_wachtwoord = row[4]

            gebruiker_lijst.append(gebruiker)  # Voeg deze gebruiker toe aan de lijst

        if id is not None:
            return gebruiker_lijst[0]  # als er geen id is meegegeven, geven we het eerste (en enige) resultaat terug
        else:
            return gebruiker_lijst  # anders geven we de hele lijst terug

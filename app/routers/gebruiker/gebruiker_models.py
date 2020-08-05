import datetime

from app.core.base_model import BaseModel

"""API request models, response models, and examples.
"""

"""Het GebruikerResponseModel is op dit moment alleen nog een hulpmiddel van de view,
   deze moet later aangevuld worden"""


class GebruikerResponseModel(BaseModel):
    id: int = 1
    gebruikersnaam: str = "gebruikersnaam"
    wachtwoord: str = "wachtwoord"
    rol: int = 0
    tijdelijk_wachtwoord: bytes = 0


"""Het TokenModel wordt in de backend gebruikt om tokens te bewaren en te verifieren"""


class TokenModel(BaseModel):
    token: str = ""
    gebruikersnaam: str = ""
    verloop: float = -1


"""Het TokenResponseModel wordt naar de front-end gestuurd"""


class TokenResponseModel(BaseModel):
    token: str = None
    tijdelijk_wachtwoord: int = 0


class RolResponseModel(BaseModel):
    id: int = 0
    rol: str = "rol"

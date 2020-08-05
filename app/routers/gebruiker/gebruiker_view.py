import sys
from typing import List

import bcrypt
from fastapi import APIRouter, HTTPException, Query, Path

from app.core.errors.additional_responses import ERROR_RESPONSE
from app.core.utils.documentation import prepare_example_response
from app.routers.gebruiker.gebruiker_controller import GebruikerController
from app.routers.overige.overige_authentication_service import AuthenticationService
from app.routers.gebruiker.gebruiker_models import GebruikerResponseModel, RolResponseModel

app = APIRouter()
controller = GebruikerController()
auth = AuthenticationService()

"""get_gebruikers haalt alle gebruikers op en stuurt deze terug"""


@app.get('/',
         response_model=List[GebruikerResponseModel], status_code=200)
async def get_gebruikers(token: str):
    if auth.can_user_access(token):
        return controller.get_gebruikers()


"""post_gebruiker maakt een nieuwe gebruiker aan en stuurt deze terug"""


@app.post('/',
          response_model=List[GebruikerResponseModel], status_code=201)
async def post_gebruiker(model: GebruikerResponseModel, token: str):
    if auth.can_user_access(token) and auth.check_of_user_is_beheerder(token):
        model.wachtwoord = auth.hash_wachtwoord(model.wachtwoord)
        return controller.create_gebruiker(model)
    raise HTTPException(status_code=405, detail="Om deze actie uit te voeren heeft u beheerdersrechten nodig")


"""update_gebruiker past de gebruiker aan en stuurt deze terug"""


@app.put('/',
         response_model=List[GebruikerResponseModel], status_code=200)
async def update_gebruiker(model: GebruikerResponseModel, token: str):
    if auth.can_user_access(token) and auth.check_of_user_is_beheerder(token):
        model.wachtwoord = auth.hash_wachtwoord(model.wachtwoord)
        return controller.update_gebruiker(model)
    else:
        raise HTTPException(status_code=405, detail="Om deze actie uit te voeren heeft u beheerdersrechten nodig")


"""delete_gebruiker verwijdert een gebruiker"""


@app.delete('/{id}/',
            response_model=List[GebruikerResponseModel], status_code=200)
async def delete_gebruiker(id: int, token: str):
    print("view:" + str(id))
    if auth.can_user_access(token) and auth.check_of_user_is_beheerder(token):
        return controller.delete_gebruiker(id)
    else:
        raise HTTPException(status_code=405, detail="Om deze actie uit te voeren heeft u beheerdersrechten nodig")


"""Ontvangt een gebruikersnaam en wachtwoord en retourneerd een token"""


@app.post('/login', status_code=200)
async def login(gebruiker: GebruikerResponseModel):
    print(gebruiker.json() + "\n\n\n")
    if auth.authenticate_user(gebruiker.gebruikersnaam, gebruiker.wachtwoord):
        return auth.generate_token(gebruiker.gebruikersnaam)


"""Ontvant een token uit de front-end en retourneerd of de token goed is of niet"""


@app.get('/verify', status_code=200)
async def verify_token(token: str):
    if auth.check_if_token_in_cache(token):
        return True


"""Ontvangt een gebruiker model met daarin alleen een wachtwoord. 
Vervolgens wordt er met de token een gebruiker opgehaald en het wachtwoord gehasht."""


@app.put('/update_password', status_code=200)
async def update_password(gebruiker: GebruikerResponseModel, token: str):
    if auth.check_if_token_in_cache(token):
        gebruiker.gebruikersnaam = auth.get_user_by_token(token)
        gebruiker.wachtwoord = auth.hash_wachtwoord(gebruiker.wachtwoord)
        controller.update_wachtwoord(gebruiker)
    else:
        raise HTTPException(status_code=401, detail="Uw token is ongeldig of verlopen")


@app.get('/is_beheerder', status_code=200)
async def is_beheerder(token: str):
    return auth.check_of_user_is_beheerder(token)


@app.get('/rollen', response_model=List[RolResponseModel], status_code=200)
async def get_rollen(token: str):
    if auth.check_of_user_is_beheerder(token):
        return controller.get_rollen()
    else:
        raise HTTPException(status_code=401, detail="U bent geen beheerder")

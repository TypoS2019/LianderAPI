#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, HTTPException, Query, Path
from starlette.status import HTTP_400_BAD_REQUEST

from app.core.errors.additional_responses import ERROR_RESPONSE
from app.core.utils.documentation import prepare_example_response
from app.routers.overige.overige_authentication_service import AuthenticationService
from app.routers.interventie.interventie_controller import InterventieController
from app.routers.interventie.interventie_models import InterventieResponseModel

app = APIRouter()

controller = InterventieController()
auth = AuthenticationService()

""" Bij ieder endpoint wordt een project_id meegegeven, deze 
wordt in de andere lagen gebruikt om specifieke data van projecten op te halen. """

"""get_interventies haalt alle interventies op en stuurt deze terug"""


@app.get('/',
         response_model=List[InterventieResponseModel], status_code=200)
async def get_interventies(project_id, token: str = ''):
    if project_id is None or project_id == 'null':
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Maak een project aan om deze pagina te bekijken",
        )
    if auth.can_user_access(token):
        return controller.get_interventies(project_id)


"""update_interventie werkt een al bestaand interventie bij en retourneert alle interventie's. """


@app.put('/',
         response_model=List[InterventieResponseModel], status_code=200)
async def update_interventie(*, model: InterventieResponseModel, project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        return controller.update_interventie(
            model, project_id)  # hier wordt het oude interventie vervangen door het meegegeven interventie


"""Toevoegen van interventie aan de lijst met interventies, geef de lijst met interventies terug"""


@app.post('/',
          response_model=List[InterventieResponseModel], status_code=201)
async def post_interventie(project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        return controller.create_interventie(InterventieResponseModel(),
                                             project_id)  # hier wordt het nieuwe interventie toegevoegd


"""Verwijderen van een interventie, geeft de lijst met interventies terus"""


@app.delete('/{interventie_id}', response_model=List[InterventieResponseModel], status_code=200)
async def delete_interventie(interventie_id: int, project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        return controller.delete_interventie(interventie_id, project_id)

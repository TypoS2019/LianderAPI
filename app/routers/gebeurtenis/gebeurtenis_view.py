#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from typing import List

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.routers.gebeurtenis.gebeurtenis_models import GebeurtenisResponseModel
from app.routers.gebeurtenis.gebeurtenis_controller import GebeurtenisController
from app.routers.overige.overige_authentication_service import AuthenticationService

"""Behandelt de REST-API Requests en Responses"""
app = APIRouter()

controller = GebeurtenisController()

auth = AuthenticationService()

""" Bij ieder endpoint wordt een project_id meegegeven, deze 
wordt in de andere lagen gebruikt om specifieke data van projecten op te halen. """

"""Get_gebeurtenissen haalt alle gebeurtenissen op en stuurt deze terug naar de client"""


@app.get('/',
         response_model=List[GebeurtenisResponseModel], status_code=200)
async def get_gebeurtenissen(project_id, token: str = ''):
    if project_id is None or project_id == 'null':
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Maak een project aan om deze pagina te bekijken",
        )
    if auth.can_user_access(token):
        return controller.get_gebeurtenissen(project_id)


"""Post_gebeurtenis voegt een nieuwe gebeurtenis toe, en retourneert vervolgens de volledige lijst
met gebeurtenissen"""


@app.post('/',
          response_model=List[GebeurtenisResponseModel], status_code=201)
async def post_gebeurtenis(*, model: GebeurtenisResponseModel, project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        return controller.post_gebeurtenis(model, project_id)


"""Delete_gebeurtenis verwijdert de gespecificeerde gebeurtenis en stuurt een lijst van gebeurtenissen terug"""


@app.delete('/{gebeurtenis_id}',
            response_model=List[GebeurtenisResponseModel], status_code=200)
async def delete_gebeurtenis(gebeurtenis_id: int, project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        return controller.delete_gebeurtenis(gebeurtenis_id, project_id)


"""Updated de gebeurtenis die meegegeven wordt en stuurt de hele lijst terug"""


@app.put('/',
         response_model=List[GebeurtenisResponseModel], status_code=200)
async def update_gebeurtenis(model: GebeurtenisResponseModel, project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        return controller.update_gebeurtenis(model, project_id)


@app.post('/{gebeurtenis_id}/add_interventie', status_code=201)
async def add_interventie_to_gebeurtenis(gebeurtenis_id: int, interventie_id: int, project_id: int = 1,
                                         token: str = ''):
    if auth.can_user_access(token):
        return controller.add_interventie_to_gebeurtenis(gebeurtenis_id, interventie_id, project_id)


@app.delete('/{gebeurtenis_id}/remove_interventie', status_code=200)
async def remove_interventie_from_gebeurtenis(gebeurtenis_id: int, interventie_id: int, project_id: int = 1,
                                              token: str = ''):
    if auth.can_user_access(token):
        return controller.remove_interventie_from_gebeurtenis(gebeurtenis_id, interventie_id, project_id)


@app.put('/{gebeurtenis_id}/update_interventie', status_code=200)
async def update_interventie_in_gebeurtenis(gebeurtenis_id: int, interventie_id: int, waarde: float,
                                            project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        return controller.update_interventie_in_gebeurtenis(gebeurtenis_id, interventie_id, waarde, project_id)

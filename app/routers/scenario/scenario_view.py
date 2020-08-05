#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
from typing import List

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from app.core.utils.documentation import prepare_example_response
from app.routers.overige.overige_authentication_service import AuthenticationService
from app.routers.interventie.interventie_models import GebeurtenisInterventieResponseModel, InterventieResponseModel
from app.routers.scenario.scenario_controller import ScenarioController
from app.routers.scenario.scenario_models import ScenarioResponseModel, BerekeningResponseModel
from app.routers.gebeurtenis.gebeurtenis_models import GebeurtenisResponseModel, ScenarioGebeurtenisResponseModel

"""Behandeld de REST API requests en responses."""

app = APIRouter()

controller = ScenarioController()

auth = AuthenticationService()

""" Bij ieder endpoint wordt een project_id meegegeven, deze 
wordt in de andere lagen gebruikt om specifieke data van projecten op te halen. """

"""get_scenario's haalt alle bestaande scenario op en stuurt deze terug."""


@app.get('/',
         response_model=List[ScenarioResponseModel], status_code=200)
async def get_scenario(project_id, token: str = ''):
    if project_id is None or project_id == 'null':
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Maak een project aan om deze pagina te bekijken",
        )

    if auth.can_user_access(token):
        return controller.get_all_scenarios(project_id)


"""post_scenario voegt een nieuw scenario toe aan de lijst met scenario's. Vervolgens retourneert deze alle 
scenario's. """


@app.post('/',
          response_model=List[ScenarioResponseModel], status_code=201)
async def post_scenario(*, model: ScenarioResponseModel, project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        controller.create_scenario(model, project_id)  # hier wordt het nieuwe scenario toegevoegd
        scenario_list: List[ScenarioResponseModel] = controller.get_all_scenarios(project_id)

        return scenario_list


"""delete_scenario verwijdert een scenario en retourneerd alle scenario's. """


@app.delete('/{scenario_id}',
            response_model=List[ScenarioResponseModel], status_code=200)
async def delete_scenario(scenario_id: int, project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        controller.delete_scenario(scenario_id, project_id)  # hier wordt het gewenste scenario verwijderd

        return controller.get_all_scenarios(project_id)


"""update_scenario werkt een al bestaand scenario bij en retourneert alle scenario's. """


@app.put('/',
         response_model=List[ScenarioResponseModel], status_code=200)
async def update_scenario(*, model: ScenarioResponseModel, project_id: int = 1, token: str = ''):
    controller.update_scenario(model,
                               project_id)  # hier wordt het oude sccenario vervangen door het meegegeven scenario
    return controller.get_all_scenarios(project_id)


"""get_scenario_by_id haalt het gewenste scenario op en retourneert deze. """


@app.get('/{scenario_id}',
         response_model=ScenarioResponseModel, status_code=200)
async def get_scenario_by_id(scenario_id: int, waccc: float = 5, waccw: float = 1, jaren: int = 100,
                             cumualatief_berekenen: bool = True, cashflow_berekenen: bool = True,
                             waardering_berekenen: bool = True, project_id=None, token: str = ''):
    if project_id is None or project_id == 'null':
        return
    if auth.can_user_access(token):
        result = controller.get_scenario_from_id(project_id, scenario_id, waccc, waccw,
                                                 jaren, cumualatief_berekenen, cashflow_berekenen,
                                                 waardering_berekenen)  # hier wordt het gewenste scenario opgehaald
        if result is None:
            raise HTTPException(status_code=404, detail='Maak een scenario om deze pagina te bekijken')
        return result


"""get_multiple_scenarios_by_id haalt de gewenste scenario's op en retourneert deze. """


@app.post('/selecteer_scenarios',
          response_model=List[ScenarioResponseModel], status_code=201)
async def get_multiple_scenarios_by_id(scenario_ids: List[int], waccc: float = 5, waccw: float = 1, jaren: int = 100,
                                       cumulatief_berekenen: bool = True, cashflow_berekenen: bool = True,
                                       waardering_berekenen: bool = True, project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        result = controller.get_multiple_scenarios_from_ids(project_id, scenario_ids, waccc, waccw, jaren,
                                                            cumulatief_berekenen, cashflow_berekenen,
                                                            waardering_berekenen)  # hier worden de gewenste scenario's opgehaald
        if not result:
            raise HTTPException(status_code=404, detail='Scenarios not found')
        return result


@app.post('/{scenario_id}/add_gebeurtenis', status_code=201)
async def add_gebeurtenis_to_scenario(scenario_id: int, gebeurtenis_id: int, project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        return controller.add_gebeurtenis_to_scenario(scenario_id, gebeurtenis_id, project_id)


@app.delete('/{scenario_id}/remove_gebeurtenis', status_code=200)
async def remove_gebeurtenis_from_scenario(scenario_id: int, gebeurtenis_id: int, project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        return controller.remove_gebeurtenis_from_scenario(scenario_id, gebeurtenis_id, project_id)


@app.post('/{scenario_id}/gebeurtenis/{gebeurtenis_id}/add_jaar', status_code=201)
async def add_jaar_to_gebeurtenis_in_scenario(scenario_id: int, gebeurtenis_id: int, jaar: int, waarde: int,
                                              project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        return controller.add_jaar_to_gebeurtenis_in_scenario(scenario_id, gebeurtenis_id, jaar, waarde, project_id)


@app.delete('/{scenario_id}/gebeurtenis/{gebeurtenis_id}/remove_jaar', status_code=200)
async def remove_jaar_from_gebeurtenis_in_scenario(scenario_id: int, gebeurtenis_id: int, jaar: int,
                                                   project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        return controller.remove_jaar_from_gebeurtenis_in_scenario(scenario_id, gebeurtenis_id, jaar, project_id)


@app.put('/{scenario_id}/gebeurtenis/{gebeurtenis_id}/update_jaar', status_code=200)
async def update_jaar_in_gebeurtenis_in_scenario(scenario_id: int, gebeurtenis_id: int, jaar: int, waarde: int,
                                                 project_id: int = 1, token: str = ''):
    if auth.can_user_access(token):
        return controller.update_jaar_in_gebeurtenis_in_scenario(scenario_id, gebeurtenis_id, jaar, waarde, project_id)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import tempfile
from asyncore import write
from typing import List

import pandas as pd
from fastapi import APIRouter, HTTPException, Query, Path, File, UploadFile
from pandas.io.formats import console
from starlette.responses import FileResponse, Response

from app.routers.overige.overige_authentication_service import AuthenticationService
from app.routers.overige.overige_models import OpslagResponseModel
from app.routers.overige.overige_controller import OverigeController
from app.routers.scenario.scenario_models import BerekeningResponseModel
from app.routers.scenario.scenario_models import ScenarioResponseModel

app = APIRouter()

controller = OverigeController()
auth = AuthenticationService()

"""get_alle_data haalt alle data op en retourneert deze."""


@app.get('/opslaan',
         response_model=OpslagResponseModel, status_code=200)
async def get_alle_data(project_id):
    return controller.collecteer_data(project_id)


"""get_alle_resultaten haalt alle resultaten van de scenarios en retourneert deze"""


@app.get('/opslaan/resultaat', response_model=List[BerekeningResponseModel], status_code=200)
async def get_alle_resultaten(project_id, waccc: float = 5, waccw: float = 1, jaren: int = 100, cumulatief_berekenen: bool = False, token: str = ""):
    if auth.can_user_access(token):
        return controller.collecteer_resultaten(project_id, waccc, waccw, jaren, cumulatief_berekenen)


""" get_excel haalt een scenario op met het ID, en geef deze terug. """


@app.get('/export/{scenario_id}', status_code=200)
async def get_excel(project_id: int, scenario_id: int, start_jaar: int, token: str = ''):
    # maak excel bestand en sla op in bin met rand naam, stuur naam terug in return waarde
    if auth.can_user_access(token):
        result = controller.get_excel(project_id, scenario_id, start_jaar)
        response = FileResponse(result)
        return response


""" delete_excel verwijderen van excel bestand """


@app.delete('/delete', status_code=200)
async def delete_excel(token: str):
    # verwijderen van excel bestand
    if auth.can_user_access(token):
        controller.delete_excel()


""" create_upload_file uploaden van excel bestand """


@app.post("/uploadfile/", status_code=200)
async def create_upload_file(file: UploadFile = File(...), project_id: int = 1, token: str = ""):
    if auth.can_user_access(token):
        json_list = []
        #Ophalen sheet namen van een excel bestand
        sheet_names = controller.get_all_excel_sheet_names(file.file)

        #De verschillende sheets omzetten naar json
        for i in range(len(sheet_names)):
            json_list.append(controller.convert_excel_sheet_to_json(file.file, sheet_names[i]))

        #Alle json importeren naar database
        controller.import_excel(json_list, project_id)
        return {"filename": file.filename + " Uploaded succesfull"}



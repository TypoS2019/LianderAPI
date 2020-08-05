from typing import List

from fastapi import APIRouter, HTTPException, Query, Path

from app.core.errors.additional_responses import ERROR_RESPONSE
from app.core.utils.documentation import prepare_example_response
from app.routers.overige.overige_authentication_service import AuthenticationService
from app.routers.project.project_controller import ProjectController
from app.routers.project.project_models import ProjectResponseModel

app = APIRouter()

auth = AuthenticationService()

"""get_projecten haalt alle projecten voor de gebruiker op en stuurt deze terug"""


@app.get('/',
         response_model=List[ProjectResponseModel], status_code=200)
async def get_projecten(token: str):
    if auth.can_user_access(token):
        gebruikersnaam = auth.get_user_by_token(token)
        return ProjectController().get_alle_projecten(gebruikersnaam)
    else:
        raise auth.forbidden_exception


"""get_project_by_id haalt het project op dat het meegegeven id heeft en stuurt deze terug"""


@app.get('/{project_id}',
         response_model=ProjectResponseModel, status_code=200)
async def get_project_by_id(project_id: int, token: str):
    if auth.can_user_access(token):
        ProjectController().get_project_by_id(project_id, token)
        return {}
    else:
        raise auth.forbidden_exception


"""post_project maak een nieuw project aan en stuurt alle projecten van de gebruiker terug"""


@app.post('/',
          response_model=List[ProjectResponseModel], status_code=201)
async def post_project(model: ProjectResponseModel, token: str):
    if auth.can_user_access(token):
        gebruikersnaam = auth.get_user_by_token(token)
        gebruiker_id = auth.get_id_by_gebruikersnaam(gebruikersnaam)
        ProjectController().create_project(model, gebruiker_id)
        return []
    else:
        raise auth.forbidden_exception


"""update_project werkt het project bij die meegestuurt wordt en stuurt alle projecten terug"""


@app.put('/',
         response_model=List[ProjectResponseModel], status_code=200)
async def update_project(model: ProjectResponseModel, token: str):
    if auth.can_user_access(token):
        ProjectController().update_project(model, token)
        return []
    else:
        raise auth.forbidden_exception


"""delete_project verwijdert het project van het meegeleverde id en stuurt alle projecten terug"""


@app.delete('/{project_id}',
            response_model=List[ProjectResponseModel], status_code=200)
async def delete_project(project_id: int, token: str):
    if auth.can_user_access(token):
        ProjectController().delete_project(project_id, token)
        return []
    else:
        raise auth.forbidden_exception


"""voeg_gebruiker_toe_aan_project voegt een gebruiker via het id toe aan het project en stuurt alle projecten terug"""


@app.post('/{project_id}/{gebruiker_id}',
          response_model=List[ProjectResponseModel], status_code=201)
async def voeg_gebruiker_toe_aan_project(project_id: int, gebruiker_id: int, token: str):
    if auth.can_user_access(token):
        ProjectController().voeg_gebruiker_toe_aan_project(project_id, gebruiker_id, token)
        return []
    else:
        raise auth.forbidden_exception


"""verwijder_gebruiker_uit_project verwijdert een gebruiker uit een project"""


@app.delete('/{project_id}/{gebruiker_id}',
            response_model=List[ProjectResponseModel], status_code=200)
async def verwijder_gebruiker_uit_project(project_id: int, gebruiker_id: int, token: str):
    if auth.can_user_access(token):
        ProjectController().verwijder_gebruiker_uit_project(project_id, gebruiker_id, token)
        return []
    else:
        raise auth.forbidden_exception

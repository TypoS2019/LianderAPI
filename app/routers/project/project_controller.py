#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from typing import List

from fastapi import HTTPException

from app.routers.interventie.interventie_models import InterventieResponseModel

from app.routers.project.project_models import ProjectResponseModel
from app.routers.gebeurtenis.gebeurtenis_models import ScenarioGebeurtenisResponseModel
from app.routers.project.project_repository import ProjectMapper

"""Classes that implement business logic / use cases regarding scenario.

Classes:
    PetController: implements pet functionality
"""


class ProjectController(object):
    def __init__(self):
        self.repository = ProjectMapper()

    """"create_project geeft het meegegeven project mee aan de repository zodat het project kan worden toegevoegd"""

    def create_project(self, model: ProjectResponseModel, gebruiker_id: int):
        # self.repository.aanroep_testen() # deze later vervangen door repository functie
        self.repository.add_project(model, gebruiker_id)

    """get_alle_projecten retourneerd alle projecten die horen bij de gebruiker van het token"""

    def get_alle_projecten(self, gebruikersnaam: str):
        return self.repository.get_alle_projecten(gebruikersnaam)

    """get_project_by_id retourneerd het gewenste project dat hoort bij het meegegeven id en de gebruiker van het 
    token """

    def get_project_by_id(self, id: int, token: str):
        return self.repository.get_project(id)

    """delete_project roept delete_project in de repository aan met het id en de token zodat het gewilde project 
    verwijderd wordt"""

    def delete_project(self, id: int, token: str):
        self.repository.delete_project(id)

    """update_project roept update_project in de repository aan en stuurt het responsemodel mee zodat het juiste 
    project bijgewerkt wordt"""

    def update_project(self, model: ProjectResponseModel, token: str):
        self.repository.update_project(model)

    """voeg_gebruiker_toe_aan_project zorgt ervoor dat in de repository er de gewenste gebruiker wordt toegvoegd aan 
    het project """

    def voeg_gebruiker_toe_aan_project(self, project_id: int, gebruiker_id: int, token: str):
        self.repository.voeg_gebruiker_toe_aan_project(project_id, gebruiker_id)

    """verwijder_gebruiker_uit_project zorgt ervoor dat de repository laag de meegegeven gebruiker uit het meegegeven 
    project wordt verwijderd """

    def verwijder_gebruiker_uit_project(self, project_id: int, gebruiker_id: int, token: str):
        self.repository.verwijder_gebruiker_uit_project(project_id, gebruiker_id, token)

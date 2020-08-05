#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Optional

from app.routers.interventie.interventie_models import InterventieResponseModel
from app.routers.interventie.interventie_repository import InterventieMapper


class InterventieController(object):
    """Body controller.

    Provides the linking layer between the view (REST API interface) and repository (storage).
    """

    def __init__(self):
        self.repository = InterventieMapper()

    """Ophalen van alle interventies"""
    def get_interventies(self, project_id: int):
       return self.repository.get_interventies(project_id)

    """"Ophalen van een interventie"""
    def get_interventie(self, uuid: str, project_id: int) -> Optional[InterventieResponseModel]:
        return self.repository.get_interventie(uuid, project_id)

    """"create_interventie geeft het meegegeven interventie mee aan de repository zodat het interventie kan worden 
    toegevoegd """
    def create_interventie(self, model: InterventieResponseModel, project_id: int):
        return self.repository.add_interventie(model, project_id)

    """update_interventie geeft het meegegeven interventie mee aan de repository zodat het meegegeven interventie bijgewerkt 
        kan worden """
    def update_interventie(self, model: InterventieResponseModel, project_id: int):
        return self.repository.update_interventie(model, project_id)

    def delete_interventie(self, interventie_id, project_id: int):
        return self.repository.delete_interventie(interventie_id, project_id)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from typing import List

from app.routers.interventie.interventie_models import InterventieResponseModel
from app.routers.overige.overige_repository import DataMapper


class InterventieMapper(DataMapper):

    """_get_interventies haalt alle interventies op uit de database"""
    def _get_interventies(self, project_id):
        result = self._data_handler("SELECT * FROM interventie i LEFT JOIN project_interventie pi on pi.interventie_id = i.id "
                                    "WHERE pi.project_id = %s", (project_id,), True)
        self.logger.info(("collected " + str(len(result)) + " interventies"), source=self.source_name)
        interventie_lijst = []

        for interventie in result:
            item = InterventieResponseModel()
            item.id = interventie[0]
            item.naam = interventie[1]
            item.type = interventie[2]
            item.eenheid = interventie[3]
            item.waarde = interventie[4]
            item.toelichting = interventie[5]

            interventie_lijst.append(item)

        return interventie_lijst
    """add_interventie voegt het meegegeven interventie toe aan de lijst met alle interventie's."""

    def add_interventie(self, model: InterventieResponseModel, project_id):
        self._stored_procedure('maak_interventie_en_stop_in_project', (model.naam, model.type, model.eenheid, model.waarde, model.toelichting, project_id)) #Stored procedure voor inserten
        self.logger.info(("added interventie with id: " + str(model.id)) + " it also has been added to project: " + str(project_id), source=self.source_name)

        return self._get_interventies(project_id)

    """delete_interventie verwijdert het interventie dat hetzelfde id heeft als het getal dat meegegeven wordt."""

    def delete_interventie(self, interventie_id: int,  project_id):
        query = "DELETE FROM interventie WHERE id = %s"
        self._data_handler(query, (interventie_id,), False)
        self.logger.info(("deleted interventie with id: " + str(interventie_id)), source=self.source_name)

        return self._get_interventies(project_id)

    """get_interventie haalt een lijst met alle interventie's op en geeft deze terug"""

    def get_interventies(self, project_id):
        return self._get_interventies(project_id)

    """get_interventie haalt een interventie met een specifiek ID op uit de database"""
    def get_interventie(self, interventie_id: int, project_id):
        interventies = self._get_interventies(project_id)
        for i in interventies:  # hier wordt het gewenste interventie verwijderd
            if int(i.id) == interventie_id:
                return i
        return None

    """update_interventie vervangt het interventie met het betreffende id door het interventie dat meegegeven wordt"""

    def update_interventie(self, model: InterventieResponseModel, project_id):
        query = "UPDATE interventie " \
                "SET naam = %s, type = %s, eenheid = %s, waarde = %s, toelichting = %s " \
                "WHERE id = %s"

        values = (model.naam, model.type, model.eenheid, model.waarde, model.toelichting, model.id)

        self._data_handler(query, values, False)
        self.logger.info(("updated interventie with id: " + str(model.id)), source=self.source_name)

        return self._get_interventies(project_id)

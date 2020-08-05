#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
from typing import List
import datetime
from app.routers.project.project_models import ProjectResponseModel
from app.routers.overige.overige_repository import DataMapper


class ProjectMapper(DataMapper):
    """_get_interventies haalt alle interventies op uit de database"""

    def _get_projecten(self, gebruikernaam: str):
        result = self._data_handler(
            "SELECT P.* FROM project P JOIN project_gebruiker PG on P.id = PG.project_id JOIN gebruiker G ON G.id = PG.gebruiker_id WHERE gebruikersnaam = %s",
            (gebruikernaam,), True)
        self.logger.info(("collected " + str(len(result)) + " projecten"), source=self.source_name)
        projecten_lijst = []

        for project in result:
            print(project)
            item = ProjectResponseModel()
            item.id = project[0]
            item.naam = project[1]
            item.datum = project[2]

            projecten_lijst.append(item)

        return projecten_lijst

    """add_project voegt het meegegeven project toe aan de lijst met alle projecten."""

    def add_project(self, model: ProjectResponseModel, gebruiker_id: int):
        if model.datum is None:
            model.datum = self._get_current_date()
        query = "INSERT INTO project (naam, datum)" \
                "VALUES (%s, %s)"
        values = (model.naam, model.datum)
        self._data_handler(query, values, False)

        id = self.get_last_project_id(model)

        self.logger.info(("added project with id: " + str(id)), source=self.source_name)
        self.voeg_gebruiker_toe_aan_project(id, gebruiker_id)
        return ""

    def _get_current_date(self):
        return datetime.datetime.now()

    """delete_project verwijdert het project dat hetzelfde id heeft als het getal dat meegegeven wordt."""

    def delete_project(self, project_id: int):
        query = "DELETE FROM project WHERE id = %s"
        self._data_handler(query, (project_id,), False)
        self.logger.info(("deleted interventie with id: " + str(project_id)), source=self.source_name)

        return ""

    """get_alle_projecten haalt alle projecten op en stuurt deze terug"""

    def get_alle_projecten(self, gebruikersnaam: str):
        return self._get_projecten(gebruikersnaam)

    """get_project haalt een interventie met een specifiek ID op uit de database"""

    def get_project(self, project_id: int):
        projecten = self._get_projecten()
        for p in projecten:  # hier wordt het gewenste project verwijderd
            if int(p.id) == project_id:
                return p
        return None

    """update_project vervangt het project met het betreffende id door het project dat meegegeven wordt"""

    def update_project(self, model: ProjectResponseModel):
        query = "UPDATE project " \
                "SET naam = %s, datum = %s " \
                "WHERE id = %s"

        values = (model.naam, model.datum, model.id)

        self._data_handler(query, values, False)
        self.logger.info(("updated project with id: " + str(model.id)), source=self.source_name)

        return self._get_projecten()

    """voeg_gebruiker_toe_aan_project voegt een gebruiker toe aan een project"""

    def voeg_gebruiker_toe_aan_project(self, project_id: int, gebruiker_id: int):
        query = "INSERT INTO project_gebruiker (gebruiker_id, project_id) VALUES (%s, %s)"
        values = (gebruiker_id, project_id)
        self._data_handler(query, values, False)
        self.logger.info(("gebruiker toegevoegd aan project met id: " + str(project_id)), source=self.source_name)
        return ""

    def verwijder_gebruiker_uit_project(self, project_id, gebruiker_id, token: str):
        query = "DELETE FROM project_gebruiker WHERE project_id = %s AND gebruiker_id = %s"
        values = (project_id, gebruiker_id,)

        self._data_handler(query, values, False)
        self.logger.info(
            ("Deleted gebruiker with ID: " + str(gebruiker_id) + " from project with ID: " + str(project_id)),
            source=self.source_name)

    def get_last_project_id(self, model: ProjectResponseModel):
        query = "SELECT id FROM project WHERE naam = %s AND datum = %s"
        values = (model.naam, model.datum,)

        result = self._data_handler(query, values, True)

        if result:
            for result_item in result:
                return result[0][0]
        else:
            return None
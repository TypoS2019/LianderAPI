#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from typing import List

from app.routers.overige.overige_repository import DataMapper, JSONParser
from app.routers.gebeurtenis.gebeurtenis_models import GebeurtenisResponseModel


class GebeurtenisMapper(DataMapper):
    """Add_scenario voegt de nieuwe gebeurtenis toe aan de lijst met gebeurtenissen"""

    def add_gebeurtenis(self, model: GebeurtenisResponseModel, project_id):
        self._stored_procedure('maak_gebeurtenis_en_stop_in_project', (
            model.naam, model.toelichting, model.bronvermelding, model.eenheid_per,
            project_id))  # Stored procedure voor inserten
        self.logger.info(
            ("added gebeurtenis with id: " + str(model.id)) + " it also has been added to project: " + str(project_id),
            source=self.source_name)
        return self.get_gebeurtenissen(project_id)

    """Get_gebeurtenis retourneert de lijst van gebeurtenissen"""

    def get_gebeurtenissen(self, project_id):
        parser = GebeurtenisJSONParser()
        return parser.get_gebeurtenissen(project_id)

    """Update_gebeurtenis updated """

    def update_gebeurtenis(self, model: GebeurtenisResponseModel, project_id):
        query = "UPDATE gebeurtenis " \
                "SET naam = %s, toelichting = %s, bron = %s, eenheid = %s " \
                "WHERE id = %s"

        values = (model.naam, model.toelichting, model.bronvermelding, model.eenheid_per, model.id)

        self._data_handler(query, values, False)
        self.logger.info(("updated gebeurtenis with id: " + str(model.id)), source=self.source_name)
        return self.get_gebeurtenissen(project_id)

    def delete_gebeurtenis(self, gebeurtenis_id: int, project_id: int):
        query = "DELETE FROM gebeurtenis WHERE id = %s"
        self._data_handler(query, (gebeurtenis_id,), False)
        self.logger.info(("deleted gebeurtenis with id: " + str(gebeurtenis_id)), source=self.source_name)
        return self.get_gebeurtenissen(project_id)

    def add_interventie_to_gebeurtenis(self, gebeurtenis_id, interventie_id, project_id):
        query = "INSERT INTO gebeurtenis_interventie(gebeurtenis_id, interventie_id) VALUES (%s, %s)"
        values = [gebeurtenis_id, interventie_id]
        self._data_handler(query, values, False)
        self.logger.info(
            ("added interventie with id: " + str(interventie_id) + " to gebeurtenis with id: " + str(gebeurtenis_id)),
            source=self.source_name)
        return self.get_gebeurtenissen(project_id)

    def update_interventie_in_gebeurtenis(self, gebeurtenis_id, interventie_id, waarde, project_id):
        query = "UPDATE gebeurtenis_interventie SET waarde = %s WHERE gebeurtenis_id = %s AND interventie_id = %s"
        values = [waarde, gebeurtenis_id, interventie_id]
        self._data_handler(query, values, False)
        self.logger.info(
            ("updated interventie with id: " + str(interventie_id) + " in gebeurtenis with id: " + str(gebeurtenis_id)),
            source=self.source_name)
        return self.get_gebeurtenissen(project_id)

    def remove_interventie_from_gebeurtenis(self, gebeurtenis_id, interventie_id, project_id):
        query = "DELETE FROM gebeurtenis_interventie WHERE gebeurtenis_id = %s AND interventie_id = %s"
        values = [gebeurtenis_id, interventie_id]
        self._data_handler(query, values, False)
        self.logger.info(("removed interventie with id: " + str(interventie_id) + " from gebeurtenis with id: " + str(
            gebeurtenis_id)), source=self.source_name)
        return self.get_gebeurtenissen(project_id)


class GebeurtenisJSONParser(JSONParser):
    """get_gebeurtenissen haalt een of alle gebeurtenissen op uit de database en zet deze om naar objecten"""

    def get_gebeurtenissen(self, project_id, gebeurtenis_id=None):
        result = self._get_queries(gebeurtenis_id, project_id)

        self.logger.info(("collected " + str(len(result)) + " gebeurtenissen"), source=self.source_name)

        gebeurtenissen = []
        gebeurtenissen_id_lijst = []
        gebeurtenis_lijst = []

        if len(
                result) > 0:  # Als er meer dan 0 resultaten zijn (voor het geval de db leeg is of er geen gebeurtenissen met het specifieke ID zijn)
            gebeurtenissen_id_lijst = self._voeg_resultaten_toe_aan_lijst(gebeurtenissen_id_lijst, result)

            gebeurtenissen_id_lijst, gebeurtenissen = self._voeg_gebeurtenis_toe_aan_lijst(gebeurtenissen_id_lijst,
                                                                                           gebeurtenissen, result)

            gebeurtenissen, gebeurtenis_lijst = self._voeg_gebeurtenis_object_toe_aan_lijst(gebeurtenissen,
                                                                                            gebeurtenis_lijst, result)

        return gebeurtenis_lijst

    def _voeg_resultaten_toe_aan_lijst(self, gebeurtenissen_id_lijst, result):
        for row in result:  # Voor ieder resultaat
            if row[0] not in gebeurtenissen_id_lijst:  # Als het ID van de gebeurtenis niet in de lijst met ID's staat
                gebeurtenissen_id_lijst.append(row[0])  # voegen we deze toe (om duplicaten te voorkomen)
        return gebeurtenissen_id_lijst

    def _voeg_gebeurtenis_toe_aan_lijst(self, gebeurtenissen_id_lijst, gebeurtenissen, result):
        for gebeurtenis_id in gebeurtenissen_id_lijst:  # voor iedere gebeurtenis in de lijst
            for row in result:
                if row[0] in gebeurtenissen_id_lijst:  # Als het ID in de lijst staat
                    gebeurtenis = self._genereer_gebeurtenis([], row, len(gebeurtenissen), [],
                                                             -9)  # maken we van deze lijn een nieuw object
                    gebeurtenissen.append(gebeurtenis)  # Voeg deze gebeurtenis toe aan de lijst met gebeurtenissen
                    gebeurtenissen_id_lijst.remove(row[0])  # En haal het ID uit de lijst met Id's
        return gebeurtenissen_id_lijst, gebeurtenissen

    def _voeg_gebeurtenis_object_toe_aan_lijst(self, gebeurtenissen, gebeurtenis_lijst, result):
        for gebeurtenis in gebeurtenissen:  # voor iedere gebeurtenis in de gebeurtenissen-lijst
            interventie_lijst = []
            for row in result:  # Voor iedere rij die uit de database komt
                if row[5] == gebeurtenis.id:  # Als de 5e waarde het ID van de gebeurtenis is
                    interventie = self._genereer_interventie(row, -9,
                                                             len(interventie_lijst))  # maak een nieuwe interventie
                    interventie_lijst.append(interventie)  # En voeg deze toe aan de lijst van interventies
            gebeurtenis.interventies = interventie_lijst  # zet de lijst met interventies in de gebeurtenissen-lijst
            gebeurtenis_lijst.append(gebeurtenis)  # En voeg deze toe aan de uiteindelijke lijst
        return gebeurtenissen, gebeurtenis_lijst

    def _get_queries(self, gebeurtenis_id, project_id):
        result = None  # Initializeer de 'result'-parameter
        if gebeurtenis_id is None:  # als er geen gebeurtenis_id mee is gegeven (en de gebruiker dus alle gebeurtenissen wil)
            query = "SELECT * FROM gebeurtenis g LEFT JOIN gebeurtenis_interventie gi on g.id = gi.gebeurtenis_id LEFT JOIN interventie i on gi.interventie_id = i.id " \
                    "LEFT JOIN  project_gebeurtenis pg ON pg.gebeurtenis_id = g.id WHERE pg.project_id = %s"

            result = self._data_handler(query, (project_id,), True)
            """Voeren we de select * query uit zonder WHERE-clause. Dit haalt alle resultaten op"""
        else:  # Als de gebruiker wel een ID mee heeft gegeven
            query = "SELECT * FROM gebeurtenis g LEFT JOIN gebeurtenis_interventie gi on g.id = gi.gebeurtenis_id LEFT JOIN interventie i on gi.interventie_id = i.id WHERE g.id = %s"

            result = self._data_handler(query, (gebeurtenis_id,), True)
            """Dan halen we de gebeurtenissen voor dat specifieke ID op uit de database."""
        return result

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from typing import List

from app.routers.overige.overige_repository import DataMapper, JSONParser
from app.routers.scenario.scenario_models import ScenarioResponseModel
from app.routers.gebeurtenis.gebeurtenis_models import ScenarioGebeurtenisResponseModel, GebeurtenisResponseModel, \
    WaardePerJaar
from app.routers.gebeurtenis.gebeurtenis_repository import GebeurtenisMapper


class ScenarioMapper(DataMapper):
    """write schrijft de lijst van scenario's die megegeven worden als json in een text bestand. """

    def _get_scenarios(self, project_id: int):
        parser = ScenarioJSONParser()

        return parser.get_scenarios_with_details(project_id)

    """add_scenario voegt het meegegeven scenario toe aan de lijst met alle scenario's."""

    def add_scenario(self, model: ScenarioResponseModel, project_id: int):
        self._stored_procedure('maak_scenario_en_stop_in_project',
                               (model.naam, model.toelichting, project_id))  # Stored procedure voor inserten
        self.logger.info(
            ("added scenario with id: " + str(model.id)) + " it also has been added to project: " + str(project_id),
            source=self.source_name)
        return self._get_scenarios(project_id)

    """delete_scenario verwijdert het scenario dat hetzelfde id heeft als het getal dat meegegeven wordt."""

    def delete_scenario(self, scenario_id: int, project_id):
        query = "DELETE FROM scenario WHERE id = %s"
        self._data_handler(query, (scenario_id,), False)
        self.logger.info(("deleted scenario with id: " + str(scenario_id)), source=self.source_name)
        return self._get_scenarios(project_id)

    """get_scenario haalt een lijst met alle scenario's op en geeft deze terug"""

    def get_scenarios(self, project_id: int):
        return self._get_scenarios(project_id)

    def get_scenario_by_id(self, id: int, project_id: int):
        parser = ScenarioJSONParser()
        return parser.get_scenarios_with_details(id, project_id)

    """update_scenario vervangt het scenario met het betreffende id door het scenario dat meegegeven wordt"""

    def update_scenario(self, model: ScenarioResponseModel, project_id):
        query = "UPDATE scenario " \
                "SET naam = %s, toelichting = %s " \
                "WHERE id = %s"

        values = (model.naam, model.toelichting, model.id)

        self._data_handler(query, values, False)
        self.logger.info(("updated scenario with id: " + str(model.id)), source=self.source_name)
        return self._get_scenarios(project_id)

    def add_gebeurtenis_to_scenario(self, scenario_id, gebeurtenis_id, project_id):
        query = "INSERT INTO scenario_gebeurtenis(scenario_id, gebeurtenis_id) VALUES (%s, %s)"
        values = [scenario_id, gebeurtenis_id]
        self._data_handler(query, values, False)
        self.logger.info(
            ("added gebeurtenis with id: " + str(gebeurtenis_id) + " to scenario with id: " + str(scenario_id)),
            source=self.source_name)
        return self._get_scenarios(project_id)

    def remove_gebeurtenis_from_scenario(self, scenario_id, gebeurtenis_id, project_id):
        query = "DELETE FROM scenario_gebeurtenis WHERE scenario_id = %s AND gebeurtenis_id = %s"
        values = [scenario_id, gebeurtenis_id]
        self._data_handler(query, values, False)
        self.logger.info(
            ("removed gebeurtenis with id: " + str(gebeurtenis_id) + " from scenario with id: " + str(scenario_id)),
            source=self.source_name)
        return self._get_scenarios(project_id)

    def add_jaar_to_gebeurtenis_in_scenario(self, scenario_id, gebeurtenis_id, jaar, waarde, project_id):
        query = "INSERT INTO jaren(koppeling_id, jaar, waarde) VALUES ((SELECT koppeling_id FROM scenario_gebeurtenis WHERE scenario_id = %s AND gebeurtenis_id = %s), %s, %s)"
        values = [scenario_id, gebeurtenis_id, jaar, waarde]
        self._data_handler(query, values, False)
        self.logger.info(("added jaar: " + str(jaar) + " to scenario_gebeurtenis with scenario_id: " + str(
            scenario_id) + " and gebeurtenis_id: " + str(gebeurtenis_id)), source=self.source_name)
        return self._get_scenarios(project_id)

    def update_jaar_in_gebeurtenis_in_scenario(self, scenario_id, gebeurtenis_id, jaar, waarde, project_id):
        query = "UPDATE jaren SET waarde = %s WHERE koppeling_id IN (SELECT koppeling_id FROM scenario_gebeurtenis WHERE scenario_id = %s AND gebeurtenis_id = %s) AND jaar = %s"
        values = [waarde, scenario_id, gebeurtenis_id, jaar]
        self._data_handler(query, values, False)
        self.logger.info(("updated jaar: " + str(jaar) + " in scenario_gebeurtenis with scenario_id: " + str(
            scenario_id) + " and gebeurtenis_id: " + str(gebeurtenis_id)), source=self.source_name)
        return self._get_scenarios(project_id)

    def remove_jaar_from_gebeurtenis(self, scenario_id, gebeurtenis_id, jaar, project_id):
        query = "DELETE FROM jaren WHERE jaar = %s AND koppeling_id IN (SELECT koppeling_id FROM scenario_gebeurtenis WHERE scenario_id = %s AND gebeurtenis_id = %s)"
        values = [jaar, scenario_id, gebeurtenis_id]
        self._data_handler(query, values, False)
        self.logger.info(("delete jaar: " + str(jaar) + " in scenario_gebeurtenis with scenario_id: " + str(
            scenario_id) + " and gebeurtenis_id: " + str(gebeurtenis_id)), source=self.source_name)
        return self._get_scenarios(project_id)


class ScenarioJSONParser(JSONParser):
    """get_scenarios_with_details genereert JSON voor een bepaald scenario"""

    def get_scenarios_with_details(self, project_id, scenario_id=None):

        result = self._get_results_for_scenarios(scenario_id, project_id)

        scenario_id_lijst = []
        scenario_lijst = []

        offset = 0
        for row in result:
            if row[0] not in scenario_id_lijst:
                scenario_id_lijst.append(row[0])

        for scenario in scenario_id_lijst:  # Voor ieder scenario
            gebeurtenissen = self._get_gebeurtenissen_voor_scenario(scenario, result)
            scenario_id_storage = []
            for row in result:
                if row[0] == scenario and row[0] not in scenario_id_storage:
                    nieuw_scenario = self._genereer_scenario(row, gebeurtenissen, offset)
                    scenario_lijst.append(nieuw_scenario)
                    scenario_id_storage.append(row[0])

        return scenario_lijst

    def _get_results_for_scenarios(self, scenario_id, project_id):
        result = None  # Initialiseer een variabele die het resultaat bij gaat houden
        if scenario_id is None:  # Als er geen scenario_id is meegegeven (willen we dus alle scenarios)
            query = "SELECT * FROM scenario s LEFT JOIN scenario_gebeurtenis sg ON s.id = sg.scenario_id LEFT JOIN jaren j " \
                    "ON sg.koppeling_id = j.koppeling_id LEFT JOIN gebeurtenis g ON g.id = sg.gebeurtenis_id " \
                    "LEFT JOIN gebeurtenis_interventie gi ON gi.gebeurtenis_id = g.id LEFT JOIN interventie i " \
                    "ON gi.interventie_id = i.id LEFT JOIN project_scenario ps ON s.id = ps.scenario_id WHERE ps.project_id = %s " \
                    "ORDER BY s.id, g.id"

            result = self._data_handler(query, (project_id,), True)  # Stuur deze query naar de server

        else:  # Er is wel een scenario_id meegegeven en er is dus wel een scenario die door de gebruiker gespecificeerd is
            query = "SELECT * FROM scenario s JOIN scenario_gebeurtenis sg ON s.id = sg.scenario_id JOIN jaren j " \
                    "ON sg.koppeling_id = j.koppeling_id JOIN gebeurtenis g ON g.id = sg.gebeurtenis_id " \
                    "JOIN gebeurtenis_interventie gi ON gi.gebeurtenis_id = g.id JOIN interventie i " \
                    "ON gi.interventie_id = i.id JOIN project_scenario ps ON ps.scenario_id = s.id WHERE s.id = %s AND ps.scenario_id = %s " \
                    "ORDER BY s.id, g.id"

            result = self._data_handler(query, (scenario_id, project_id), True)  # Stuur deze query naar de server
        return result

    def _get_gebeurtenissen_voor_scenario(self, scenario_id, result_set):
        gebeurtenissen_lijst = []  # Initialiseer de totale lijst van gebeurtenissen
        gebeurtenissen_id_lijst = []  # Initialiseer de lijst met gebeurtenis_id's om duplicaten te voorkomen
        offset = 0  # De offset is 0, dit heeft te maken met de query

        interventie_lijst = []  # Initialiseer de lijst van interventies per gebeurtenis
        interventie_id_lijst = []  # Initialiseer de lijst van interventie_id's per gebeurtenis

        jaren_lijst = []  # Initialiseer de totale lijst van jaren bij die gebeurtenis

        laatste_id = -1  # initialiseer die bijhoudt of het laatste gebeurtenis_id gelijk is aan het huidige
        for i, row in enumerate(result_set):  # Voor iedere meegegeven rij
            if row[0] == scenario_id:
                huidige_gebeurtenis_id = row[4]

                interventie_lijst, jaren_lijst, interventie_id_lijst = self._genereer_lijsten(huidige_gebeurtenis_id,
                                                                                              interventie_id_lijst,
                                                                                              interventie_lijst,
                                                                                              jaren_lijst, laatste_id,
                                                                                              offset, row)

                volgende_gebeurtenis_id = -1  # Initialiseer de waarde van het ID van de volgende gebeurtenis

                if len(result_set) > i + 1:  # Als de lijst nog een volgende waarde heeft
                    volgende_gebeurtenis_id = result_set[i + 1][
                        4]  # Is de volgende gebeurtenis het gebeurtenis_ID daarvan

                if volgende_gebeurtenis_id != huidige_gebeurtenis_id:
                    # De index van de gebeurtenis (het eerste ID) is de lengte van de totale lijst van gebeurtenissen
                    index = len(gebeurtenissen_lijst)
                    # We genereren een GebeurtenisInterventie object
                    gebeurtenis = self._genereer_gebeurtenis_voor_scenario(interventie_lijst, row, index, jaren_lijst,
                                                                           offset)

                    if gebeurtenis.Gebeurtenis.id not in gebeurtenissen_id_lijst:  # Als dit ID niet al in de lijst staat
                        gebeurtenissen_id_lijst.append(gebeurtenis.Gebeurtenis.id)  # Voegen we het ID toe aan die lijst
                        gebeurtenissen_lijst.append(gebeurtenis)  # En zetten we de gebeurtenis in de lijst daarvan

                laatste_id = huidige_gebeurtenis_id  # Het laatste id die we hebben gehad is het ID waar we nu mee bezig zijn
        return gebeurtenissen_lijst

    def _genereer_lijsten(self, huidige_gebeurtenis_id, interventie_id_lijst, interventie_lijst, jaren_lijst,
                          laatste_id,
                          offset, row):
        if not laatste_id == huidige_gebeurtenis_id:  # Als het niet dezelfde gebeurtenis betreft als de vorige
            interventie_lijst = []  # Gooi dan de lijst met interventies leeg (het gaat om een nieuwe gebeurtenis)
            interventie_id_lijst = []  # En doe hetzelfde voor de interventie_id's
            jaren_lijst = []  # Ook de jaren-lijst wordt gereset
        interventie_index = len(
            interventie_lijst)  # Het eerste ID van de interventie is gelijk aan de lengte van de list
        interventie = self._genereer_interventie(row, offset,
                                                 interventie_index)  # Maak een nieuwe interventie aan voor deze rij
        if interventie.interventie.id not in interventie_id_lijst:  # Als de interventie niet al in de lijst staat
            interventie_lijst.append(interventie)  # Zetten we deze interventie in de lijst
            interventie_id_lijst.append(
                interventie.interventie.id)  # En zorgen we dat dat niet nog een keer gebeurt
        jaar = self._genereer_jaar(row, offset)  # Maak een jaar van de huidige rij
        dubbel_jaar = False  # Initialiseer een boolean die bijhoudt of het jaar al in de lijst staat
        for jaar_in_lijst in jaren_lijst:  # Voor ieder jaar die al in de lijst staat
            if jaar_in_lijst.waarde == jaar.waarde and jaar_in_lijst.jaar == jaar.jaar:  # Als de waarde voor dat
                # item gelijk is aan de nieuwe en als het jaar voor het item hetzelfde is
                dubbel_jaar = True  # Bestaat het jaar dus al
        if not dubbel_jaar:  # Als het jaar nog niet bestaat
            jaren_lijst.append(jaar)  # Voeg het jaar dan toe aan de lijst
        return interventie_lijst, jaren_lijst, interventie_id_lijst

    def _genereer_scenario(self, row, gebeurtenissen, offset):
        scenario_object = ScenarioResponseModel()
        scenario_object.id = row[0]
        scenario_object.naam = row[1]
        scenario_object.toelichting = row[2]
        scenario_object.gebeurtenissen = gebeurtenissen

        return scenario_object

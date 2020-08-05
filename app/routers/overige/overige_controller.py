#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from typing import List
import random
import pandas as pd
import shutil
import time
import os

from fastapi import HTTPException

from app.routers.interventie.interventie_models import InterventieResponseModel
from app.routers.interventie.interventie_repository import InterventieMapper
from app.routers.overige.overige_models import OpslagResponseModel
from app.routers.scenario.scenario_controller import ScenarioController, LCVCalculator
from app.routers.scenario.scenario_models import ScenarioResponseModel, BerekeningResponseModel
from app.routers.gebeurtenis.gebeurtenis_controller import GebeurtenisController
from app.routers.gebeurtenis.gebeurtenis_models import GebeurtenisResponseModel
from app.routers.gebeurtenis.gebeurtenis_repository import GebeurtenisMapper
from app.routers.scenario.scenario_repository import ScenarioMapper


class OverigeController(object):
    """collecteer_data verzamelt alle gegevens die nodig zijn voor het opslaan en retourneert deze."""

    def collecteer_data(self, project_id):
        repo_scenario = ScenarioController()
        repo_gebeurtenis = GebeurtenisController()

        model = OpslagResponseModel

        model.scenarios = repo_scenario.get_all_scenarios(project_id)  # hier worden alle scenario's opgehaald
        model.gebeurtenissen = repo_gebeurtenis.get_gebeurtenissen(project_id)  # hier worden alle gebeurtenissen opgehaald
        model.interventies = []  # hier worden alle interventies opgehaald

        return model

    """collecteer_resultaten haalt alle scenarios op en berekent dan voor ieder scenario het resultaat en retourneert 
    de resultaten """

    def collecteer_resultaten(self, project_id, waccc: float = 5, waccw: float = 1, jaren: int = 100,
                              cumulatief_berekenen: bool = False):
        lcv_calc = LCVCalculator(waccc, waccw, cumulatief_berekenen)
        resultaten: List[BerekeningResponseModel] = []
        scenarios = ScenarioController().get_all_scenarios(project_id)

        for scenario in scenarios:
            resultaten.append(lcv_calc.bereken_lcv_voor_scenario(scenario, jaren))

        return resultaten

    """collecteer_resultaten_voor_scenario haalt alle scenarios op en berekent dan voor het scenario het resultaat en 
    retourneert de resultaten """

    def collecteer_resultaten_voor_scenario(self, project_id, scenario_id: int, waccc: float = 5, waccw: float = 1,
                                            jaren: int = 100,
                                            cumulatief_berekenen: bool = False):
        lcv_calc = LCVCalculator(waccc, waccw, cumulatief_berekenen)
        resultaten: BerekeningResponseModel
        scenario = ScenarioController().get_scenario_from_id(project_id, scenario_id)

        resultaten = lcv_calc.bereken_lcv_voor_scenario(scenario, jaren)

        return resultaten

    """ 
    get_excel roept aan de hand van een scenario ID de bijbehorende scenario op.
    Vervolgens word het scenario als export data opgeslagen. De opgeslagen scenario
    word in een panda dataframe opgeslagen. Er is een willekeurige naam generator gebruikt
    om een naam te koppelen aan het Excel bestand. De variable out_path, is de locatie 
    waar het bestand opgeslagen wordt. df.to_excel, kan gebruikt worden om de naam 
    van het excel sheet aan te passen. writer.save() slaat het uiteindelijk op.
    De naam van het path wordt terug gegeven aan het eind van deze functie,
    om verder te gebruiken in de view. Dit omdat de naam willekeurig is, en de view deze gebruikt.
    """

    def get_excel(self, project_id, scenario_id, startjaar=2020, aantal_jaren=100):
        self.create_bin()
        resultaten = self.collecteer_resultaten_voor_scenario(project_id, scenario_id)

        jaren = self._get_alle_jaren(startjaar, aantal_jaren)
        lcv = self._get_lcv_lijst(resultaten, aantal_jaren)
        lcc = self._get_lcc_lijst(resultaten, aantal_jaren)
        waardering = self._get_waardering_lijst(resultaten, aantal_jaren)

        lcv.append(self._get_sum(lcv))
        lcc.append(self._get_sum(lcc))
        waardering.append(self._get_sum(waardering))

        jaren.append('totaal')

        df1 = pd.DataFrame(columns=['scenario', resultaten.scenario_naam])
        df2 = pd.DataFrame(columns=jaren, index=['lcv', 'lcc', 'waardering'], data=[lcv, lcc, waardering])

        return self._schrijf_dataframe_naar_excel(df1, df2)

    """_get_alle_jaren geeft een lijst met jaartallen terug"""
    def _get_alle_jaren(self, startjaar, aantal_jaren):
        jaren = []
        for i in range(0, aantal_jaren):
            jaren.append(startjaar + i)
            i += 1
        return jaren

    """_get_lcv_lijst geeft een lijst terug met alle lcv waardes"""
    def _get_lcv_lijst(self, resultaten: BerekeningResponseModel, aantal_jaren):
        lcv = []
        for i in range(0, aantal_jaren):
            lcv.append(resultaten.lcv_per_jaar[i])
            i += 1
        return lcv

    """_get_lcc_lijst geeft een lijst terug met alle lcc waardes"""
    def _get_lcc_lijst(self, resultaten: BerekeningResponseModel, aantal_jaren):
        lcc = []
        for i in range(0, aantal_jaren):
            lcc.append(resultaten.lcc_per_jaar[i])
            i += 1
        return lcc

    """_get_waardering_lijst geeft een lijst terug met alle waardering waardes"""
    def _get_waardering_lijst(self, resultaten: BerekeningResponseModel, aantal_jaren):
        waardering = []
        for i in range(0, aantal_jaren):
            waardering.append(resultaten.waardering_per_jaar[i])
            i += 1
        return waardering

    """_get_sum geeft de som terug van de nummers uit de meegegeven lijst"""
    def _get_sum(self, waardes: List):
        return sum(waardes)

    """_random_name_generator maakt een random string aan met nummer en stuurt deze terug"""
    def _random_name_generator(self):
        # Random naam genereren voor het excel bestand in de back-end
        number = random.randrange(1000, 9999)
        randomnaam = (int(time.time())) * number
        return randomnaam

    """_schrijf_dataframe_naar_excel zet de meegegeven dataframes in een excel bestand en geeft deze terug"""
    def _schrijf_dataframe_naar_excel(self, df1, df2):
        random_naam = self._random_name_generator()

        # Maak een Pandas excel writer met de XlsxWriter engine.
        out_path = "bin/resultaat_" + str(random_naam) + ".xlsx"
        writer = pd.ExcelWriter(out_path, engine='xlsxwriter')

        # Zet dataframe om naar XlsxWriter Excel object.
        df1.to_excel(writer, sheet_name='Resultaat', startcol=-1)
        df2.to_excel(writer, sheet_name='Resultaat', startcol=1, startrow=2)

        # Haal het XlsxWriter object van het dataframe writer object.
        workbook = writer.book

        # Naam geven aan een Excel sheet.
        worksheet = writer.sheets['Resultaat']

        # Sluit het Pandas Excel writer en save de output naar een Excel file.
        writer.save()
        return out_path

    """delete_excel verwijdert de bin map"""
    def delete_excel(self):
        shutil.rmtree("bin")
        self.create_bin()

    """create_bin maakt een nieuwe bin map aan"""
    def create_bin(self):
        if not os.path.exists("bin/"):
            os.makedirs("bin/")

    """ Ophalen van alle excel Sheet namen """
    def get_all_excel_sheet_names(self, file):
        data = pd.ExcelFile(file)
        return data.sheet_names


    """ Convert excel to json """
    def convert_excel_sheet_to_json(self, file, sheet_name):
        #excel sheet met pandas in een data_string zetten
        data_string = pd.read_excel(file, sheet_name=sheet_name)
        #losse sheets omzetten naar json
        data_json = json.loads(data_string.to_json())
        return data_json


    """ Json data in responsemodel stoppen. """
    def json_model_array_gebeurtenis(self, data_json):
        json_model_array = []

        #alle data uit een json in een ResponseModel opslaan
        for i in range(len(data_json["Naam_gebeurtenis"])):
            model = GebeurtenisResponseModel()
            model.id = i
            model.naam = "Naam gebeurtenis" if data_json["Naam_gebeurtenis"][str(i)] is None else data_json["Naam_gebeurtenis"][str(i)]
            model.toelichting = "Toelichting gebeurtenis" if data_json["Toelichting_gebeurtenis"][str(i)] is None else data_json["Toelichting_gebeurtenis"][str(i)]
            model.bronvermelding = "Bronvermelding gebeurtenis" if data_json["Bron_gebeurtenis"][str(i)] is None else data_json["Bron_gebeurtenis"][str(i)]
            model.eenheid_per = "Eenheid gebeurtenis" if data_json["Eenheid_gebeurtenis"][str(i)] is None else data_json["Eenheid_gebeurtenis"][str(i)]


            #model in een array van models zetten
            json_model_array.append(model)
        return json_model_array


    """ Json data in responsemodel stoppen. """
    def json_model_array_interventie(self, data_json):
        json_model_array = []

        for i in range(len(data_json["Naam_interventie"])):
                model = InterventieResponseModel()
                model.id = i
                model.naam = "Interventie naam" if data_json["Naam_interventie"][str(i)] is None else data_json["Naam_interventie"][str(i)]
                model.type = "w" if data_json["Type_interventie"][str(i)] is None else data_json["Type_interventie"][str(i)]
                model.eenheid = "Interventie Eenheid" if data_json["Eenheid_interventie"][str(i)] is None else data_json["Eenheid_interventie"][str(i)]
                model.waarde = 0 if data_json["Waarde_interventie"][str(i)] is None else data_json["Waarde_interventie"][str(i)]
                model.toelichting = "Interventie toelichting" if data_json["Toelichting_interventie"][str(i)] is None else data_json["Toelichting_interventie"][str(i)]
                json_model_array.append(model)
        return json_model_array

    """ Json data in responsemodel stoppen. """
    def json_model_array_scenario(self, data_json):
        json_model_array = []

        for i in range(len(data_json["Naam_scenario"])):
            model = ScenarioResponseModel()
            model.id = i
            model.naam = "Scenario naam" if data_json["Naam_scenario"][str(i)] is None else data_json["Naam_scenario"][str(i)]
            model.toelichting = "Scenario toelichting" if data_json["Toelichting_scenario"][str(i)] is None else data_json["Toelichting_scenario"][str(i)]
            json_model_array.append(model)
        return json_model_array


    """ in database zetten van Json models gebeurtenis """
    def import_to_db_gebeurtenis(self, json_model_array, project_id):
        mapper = GebeurtenisMapper()
        for i in range(len(json_model_array)):
            mapper.add_gebeurtenis(json_model_array[i], project_id)


    """ in database zetten van Json models interventie """
    def import_to_db_interventie(self, json_model_array, project_id):
        mapper = InterventieMapper()
        for i in range(len(json_model_array)):
            mapper.add_interventie(json_model_array[i], project_id)


    """ in database zetten van Json models scenario """
    def import_to_db_scenario(self, json_model_array, project_id):
        mapper = ScenarioMapper()
        for i in range(len(json_model_array)):
            mapper.add_scenario(json_model_array[i], project_id)

    def import_excel(self, json_list, project_id):
        self.import_to_db_gebeurtenis(self.json_model_array_gebeurtenis(json_list[0]), project_id)
        self.import_to_db_interventie(self.json_model_array_interventie(json_list[1]), project_id)
        self.import_to_db_scenario(self.json_model_array_scenario(json_list[2]), project_id)


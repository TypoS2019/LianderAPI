import json
from typing import List
import configparser

import mysql.connector
import structlog
from fastapi import HTTPException

from app.routers.gebeurtenis.gebeurtenis_models import GebeurtenisResponseModel, WaardePerJaar
from app.routers.interventie.interventie_models import InterventieResponseModel, GebeurtenisInterventieResponseModel
from app.routers.scenario.scenario_models import ScenarioGebeurtenisResponseModel


class DataMapper:
    def __init__(self):
        self.logger = structlog.get_logger(__name__)
        self.source_name = "data-mapper"
        self.database_exception = Database_exception()

    def _db_connection(self):  # private function die de database connectie ophaalt

        config = configparser.ConfigParser()

        config.read('config.ini')

        return mysql.connector.connect(  # Maak een nieuwe connection aan
            host=config.get('DatabaseSection', 'database.host'),
            user=config.get('DatabaseSection', 'database.user'),
            password=config.get('DatabaseSection', 'database.password'),
            database=config.get('DatabaseSection', 'database.dbname')
        )

    def _stored_procedure(self, proc_name: str, parameters: tuple):
        try:
            database = self._db_connection()
            cursor = database.cursor(buffered=True)
            cursor.callproc(proc_name, parameters)
            database.commit()
            database.close()
            return "return_value"

        except mysql.connector.Error as err:
            self.logger.error("Er ging iets fout met de database: " + err.msg, source=self.source_name)
            raise self.database_exception.return_exception_message_based_on_err(err.msg)

    def _data_handler(self, sql: str, val, result: bool):  # Private method die de SQL-queries uitvoert
        try:
            self.logger.info(("executed query: '" + sql + "' with parameters: " + str(val)), source=self.source_name)
            database = self._db_connection()
            cursor = database.cursor(buffered=True)
            cursor.execute(sql, val)

            if result:
                return_value = cursor.fetchall()
            else:
                return_value = None

            database.commit()
            database.close()
            return return_value

        except mysql.connector.Error as err:
            self.logger.error("Er ging iets fout met de database: " + err.msg, source=self.source_name)
            raise self.database_exception.return_exception_message_based_on_err(err.msg)


class JSONParser(DataMapper):
    """_genereer_jaar is een private method die een rij omzet naar een WaardePerJaar klasse"""

    def _genereer_jaar(self, row, offset):
        jaar = WaardePerJaar()

        jaar.jaar = row[7]
        jaar.waarde = row[8]

        return jaar

    """_genereer_interventie is een private method die een rij omzet naar een InterventieResponseModel klasse"""

    def _genereer_interventie(self, row, offset, index):
        interventie_koppeling = GebeurtenisInterventieResponseModel()
        interventie_koppeling.id = index
        interventie_koppeling.waarde = row[16 + offset]

        interventie = InterventieResponseModel()
        interventie.id = row[15 + offset]
        interventie.type = row[19 + offset]
        interventie.eenheid = row[20 + offset]
        interventie.naam = row[18 + offset]
        interventie.waarde = row[21 + offset]
        interventie.toelichting = row[22 + offset]

        interventie_koppeling.interventie = interventie
        return interventie_koppeling

    """_genereer_gebeurtenis is een private method die een rij omzet naar een ScenarioGebeurtenis klasse"""

    def _genereer_gebeurtenis(self, interventie_lijst, row, index, jaren, offset):
        gebeurtenis = GebeurtenisResponseModel()
        gebeurtenis.id = row[9 + offset]
        gebeurtenis.naam = row[10 + offset]
        gebeurtenis.toelichting = row[11 + offset]
        gebeurtenis.bronvermelding = row[12 + offset]
        gebeurtenis.eenheid_per = row[13 + offset]
        gebeurtenis.interventies = interventie_lijst

        return gebeurtenis

    """_genereer_gebeurtenis is een private method die een rij omzet naar een ScenarioGebeurtenisResponseModel klasse"""

    def _genereer_gebeurtenis_voor_scenario(self, interventie_lijst, row, index, jaren, offset):
        GEBEURTENIS_ID_INDEX = (4 + offset)
        GEBEURTENIS_NAAM_INDEX = (10 + offset)
        GEBEURTENIS_TOELICHTING_INDEX = (11 + offset)
        GEBEURTENIS_BRON_INDEX = (12 + offset)
        GEBEURTENIS_EENHEID_INDEX = (13 + offset)

        gebeurtenis_model = ScenarioGebeurtenisResponseModel()
        gebeurtenis_model.id = index

        gebeurtenis = GebeurtenisResponseModel()
        gebeurtenis.id = row[GEBEURTENIS_ID_INDEX]
        gebeurtenis.naam = row[GEBEURTENIS_NAAM_INDEX]
        gebeurtenis.toelichting = row[GEBEURTENIS_TOELICHTING_INDEX]
        gebeurtenis.bronvermelding = row[GEBEURTENIS_BRON_INDEX]
        gebeurtenis.eenheid_per = row[GEBEURTENIS_EENHEID_INDEX]
        gebeurtenis.interventies = interventie_lijst

        gebeurtenis_model.jaren = jaren

        gebeurtenis_model.Gebeurtenis = gebeurtenis
        return gebeurtenis_model


class Database_exception:

    """ Deze klasse wordt gebruikt om een duidelijk bericht te 'raisen' bij het verkrijgen van een exception die te
    maken heeft met de DB """
    connection_failed = HTTPException(status_code=503, detail='Er kon geen database connectie gemaakt worden')
    type_niet_goed = HTTPException(status_code=500, detail='Er zit een fout in uw Excel sheet. \n')
    geen_data_gevonden = HTTPException(status_code=404, detail='Er kon geen data worden opgehaald.')

    def return_exception_message_based_on_err(self, err: str):
        if err.__contains__('denied'):
            return self.connection_failed
        elif err.__contains__('truncated'):
            return self.type_niet_goed
        else:
            return self.geen_data_gevonden

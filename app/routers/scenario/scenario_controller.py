#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from typing import List

from fastapi import HTTPException

from app.routers.interventie.interventie_models import InterventieResponseModel
from app.routers.scenario.scenario_repository import ScenarioMapper

from app.routers.scenario.scenario_models import ScenarioResponseModel, BerekeningResponseModel, \
    GebeurtenisMetWaardesPerJaar, InterventieMetWaardesPerJaar
from app.routers.gebeurtenis.gebeurtenis_models import ScenarioGebeurtenisResponseModel

"""Classes that implement business logic / use cases regarding scenario.

Classes:
    PetController: implements pet functionality
"""


class ScenarioController(object):

    def __init__(self):
        self.repository = ScenarioMapper()
        self.scenarios = []
        self.JAREN = 100

    """"create_scenario geeft het meegegeven scenario mee aan de repository zodat het scenario kan worden toegevoegd"""

    def create_scenario(self, model: ScenarioResponseModel, project_id: int):
        self.repository.add_scenario(model, project_id)

    """get_all_scenario's roept get_scenarios() aan in de repository en geeft alle opgehaalde scenarios terug"""

    def get_all_scenarios(self, project_id: int):
        return self.repository.get_scenarios(project_id)

    """delete_scenario geeft het meegegeven id mee aan de repository zodat die scenario met het meegegeven id kan 
    verwijderen """

    def delete_scenario(self, id: int, project_id: int):
        return self.repository.delete_scenario(id, project_id)

    """update_scenario geeft het meegegeven scenario mee aan de repository zodat het meegegeven scenario bijgewerkt 
    kan worden """

    def update_scenario(self, model: ScenarioResponseModel, project_id: int):
        return self.repository.update_scenario(model, project_id)

    """get_scenario_from_id selecteert het gewenste scenario en geeft deze terug."""

    def add_gebeurtenis_to_scenario(self, scenario_id, gebeurtenis_id, project_id):
        return self.repository.add_gebeurtenis_to_scenario(scenario_id, gebeurtenis_id, project_id)

    """verwijder een gebeurtenis van een scenario"""

    def remove_gebeurtenis_from_scenario(self, scenario_id, gebeurtenis_id, project_id: int):
        return self.repository.remove_gebeurtenis_from_scenario(scenario_id, gebeurtenis_id, project_id)

    """voeg een jaar toe aan een gebeurtenis binnen een scenario"""

    def add_jaar_to_gebeurtenis_in_scenario(self, scenario_id, gebeurtenis_id, jaar, waarde, project_id):
        return self.repository.add_jaar_to_gebeurtenis_in_scenario(scenario_id, gebeurtenis_id, jaar, waarde,
                                                                   project_id)

    """pas de waarde van een jaar aan"""

    def update_jaar_in_gebeurtenis_in_scenario(self, scenario_id, gebeurtenis_id, jaar, waarde, project_id):
        return self.repository.update_jaar_in_gebeurtenis_in_scenario(scenario_id, gebeurtenis_id, jaar, waarde,
                                                                      project_id)

    """verwijder een jaar uit een gebeurtenis"""

    def remove_jaar_from_gebeurtenis_in_scenario(self, scenario_id, gebeurtenis_id, jaar, project_id):
        return self.repository.remove_jaar_from_gebeurtenis(scenario_id, gebeurtenis_id, jaar, project_id)

    def get_scenario_from_id(self, project_id: int, id: int, waccc: float = 5, waccw: float = 1, jaren: int = 100,
                             cumulatief_berekenen: bool = True, cashflow_berekenen: bool = True,
                             waardering_berekenen: bool = True):
        calc = LCVCalculator(waccc, waccw, cumulatief_berekenen, cashflow_berekenen, waardering_berekenen)
        list = self.repository.get_scenarios(project_id)
        for scenario in list:
            if self._is_id_gelijk(scenario.id, id):
                scenario.result = calc.bereken_lcv_voor_scenario(scenario, jaren)
                return scenario
        return None

    """get_multiple_scenarios_from_ids selecteert de gewenste scenario's en geeft deze terug."""

    def get_multiple_scenarios_from_ids(self, project_id: int, ids: List[int], waccc: float = 5, waccw: float = 1,
                                        jaren: int = 100,
                                        cumulatief_berekenen: bool = True, cashflow_berekenen: bool = True,
                                        waardering_berekenen: bool = True):
        calc = LCVCalculator(waccc, waccw, cumulatief_berekenen, cashflow_berekenen, waardering_berekenen)
        list = self.repository.get_scenarios(project_id)
        geselecteerde_scenarios: List[ScenarioResponseModel] = []
        for id in ids:
            for scenario in list:
                if self._is_id_gelijk(scenario.id, id):
                    scenario.result = calc.bereken_lcv_voor_scenario(scenario, jaren)
                    geselecteerde_scenarios.append(scenario)
        return geselecteerde_scenarios

    def _is_id_gelijk(self, scenario_id, opgegeven_id):
        return scenario_id == opgegeven_id

class BerekeningResponseModelFiller:
    """voeg_gebeurtenis_toe_aan_berekening_model voegt een gebeurtenis met zijn waardes toe aan het berekening
        response model. Wanneer het gegeven gebeurtenis niet bestaat wordt er een nieuw model aangemaakt en toegevoegd,
        anders wordt de waarde aan de bestaande gebeurtenis toegevoegd. """

    def voeg_gebeurtenis_toe_aan_berekening_model(self, berekening_model: BerekeningResponseModel, kosten: float,
                                                  scenario_gebeurtenis: ScenarioGebeurtenisResponseModel, jaar):
        gebeurtenis_naam = scenario_gebeurtenis.Gebeurtenis.naam
        for i in range(len(berekening_model.gebeurtenis_met_waardes_per_jaar)):
            gebeurtenis = berekening_model.gebeurtenis_met_waardes_per_jaar[i]
            if gebeurtenis.gebeurtenis_naam == gebeurtenis_naam:
                gebeurtenis.waardes_per_jaar[jaar] += kosten
                return None

        model = self._prepareer_nieuw_model("gebeurtenis", gebeurtenis_naam)

        model.waardes_per_jaar[jaar] += kosten
        berekening_model.gebeurtenis_met_waardes_per_jaar.append(model)

    """voeg_interventie_toe_aan_berekening_model voegt een interventie met zijn waardes toe aan het berekening 
    response model. Wanneer het gegeven interventie niet bestaat wordt er een nieuw model aangemaakt en toegevoegd, 
    anders wordt de waarde aan de bestaande interventie toegevoegd. """

    def voeg_interventie_toe_aan_berekening_model(self, berekening_model: BerekeningResponseModel, kosten: float,
                                                  interventie: InterventieResponseModel, jaar):
        interventie_naam = interventie.naam
        for i in range(len(berekening_model.interventie_met_waardes_per_jaar)):
            interventie = berekening_model.interventie_met_waardes_per_jaar[i]
            if interventie.interventie_naam == interventie_naam:
                interventie.waardes_per_jaar[jaar] += kosten
                return None

        model = self._prepareer_nieuw_model("interventie", interventie_naam)

        model.waardes_per_jaar[jaar] += kosten
        berekening_model.interventie_met_waardes_per_jaar.append(model)

    """_prepareer_nieuw_model is een factory voor het aanmaken van een ResponseModel voor gebeurtenissen met waardes 
    per jaar of interventies met waardes per jaar. Na het aanmaken wordt het model voor 100 jaar gevuld met de waarde 
    0. Dit wordt gedaan om 100 indexes vrij te geven."""

    def _prepareer_nieuw_model(self, model_type: str, attribuut_naam: str):
        model = None
        aantal_jaren = 100
        if model_type == "gebeurtenis":
            model = GebeurtenisMetWaardesPerJaar()
            model.gebeurtenis_naam = attribuut_naam
        elif model_type == "interventie":
            model = InterventieMetWaardesPerJaar()
            model.interventie_naam = attribuut_naam

        for i in range(aantal_jaren):
            model.waardes_per_jaar.append(0)

        return model

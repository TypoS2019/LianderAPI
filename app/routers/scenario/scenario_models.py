#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from app.core.base_model import BaseModel
from app.routers.gebeurtenis.gebeurtenis_models import ScenarioGebeurtenisResponseModel


class InterventieMetWaardesPerJaar(BaseModel):
    interventie_naam = "naam"
    waardes_per_jaar: List[float] = []


class GebeurtenisMetWaardesPerJaar(BaseModel):
    gebeurtenis_naam = "naam"
    waardes_per_jaar: List[float] = []


"""LCCResponseModel beschrijft alle eigenschappen van het resultaat van de LCC berekening """


class BerekeningResponseModel(BaseModel):
    scenario_naam: str = "naam"
    lcc_per_jaar: List[float] = []
    lcv_per_jaar: List[float] = []
    waardering_per_jaar: List[float] = []
    gebeurtenis_met_waardes_per_jaar: List[GebeurtenisMetWaardesPerJaar] = []
    interventie_met_waardes_per_jaar: List[InterventieMetWaardesPerJaar] = []
    eaw_per_jaar: List[float] = []


"""ScenarioResponseModel beschrijft alle eigenschappen van een scenario"""


class ScenarioResponseModel(BaseModel):
    id: int = 1
    naam: str = "scenario"
    toelichting: str = "toelichting"
    result: BerekeningResponseModel = None
    gebeurtenissen: List[ScenarioGebeurtenisResponseModel] = []

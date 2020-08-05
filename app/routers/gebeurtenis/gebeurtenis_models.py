#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from app.core.base_model import BaseModel
from app.routers.interventie.interventie_models import GebeurtenisInterventieResponseModel

"""API request models, response models, and examples.
"""


class GebeurtenisResponseModel(BaseModel):
    id: int = 1
    naam: str = "naam"
    toelichting: str = "toelichting"
    bronvermelding: str = "bronvermelding"
    eenheid_per: str = "eenheid_per"
    interventies: List[GebeurtenisInterventieResponseModel] = []


class WaardePerJaar(BaseModel):
    waarde: float = 1
    jaar: int = 1


class ScenarioGebeurtenisResponseModel(BaseModel):
    id: int = 1
    Gebeurtenis: GebeurtenisResponseModel = None
    jaren: List[WaardePerJaar] = []

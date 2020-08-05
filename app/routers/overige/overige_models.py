#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from app.core.base_model import BaseModel
from app.routers.interventie.interventie_models import InterventieResponseModel
from app.routers.scenario.scenario_models import ScenarioResponseModel
from app.routers.gebeurtenis.gebeurtenis_models import GebeurtenisResponseModel

"""OpslagResponseModel beschrijft alle eigenschappen die nodig zijn voor het opslaan van alle scenario's 
gebeurtenissen en interventies. """


class OpslagResponseModel(BaseModel):
    scenarios: List[ScenarioResponseModel]
    gebeurtenissen: List[GebeurtenisResponseModel]
    interventies: List[InterventieResponseModel]

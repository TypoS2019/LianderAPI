#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.core.base_model import BaseModel

"""API request models, response models, and examples.
"""


class InterventieResponseModel(BaseModel):
    id: int = 1
    type: str = 'c'
    eenheid: str = "$"
    naam: str = "CAPEX"
    waarde: float = 1
    toelichting: str = 'toelichting'


class GebeurtenisInterventieResponseModel(BaseModel):
    id: int = 1
    interventie: InterventieResponseModel = None
    waarde: float = 0


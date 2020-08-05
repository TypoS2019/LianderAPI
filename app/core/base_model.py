#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    """Base model for API request and response models.

    Introduced after the upgrade of FastAPI to 0.30.0, which required the use of
    the orm_mode attribute, to maintain its behavior: https://fastapi.tiangolo.com/release-notes/#0300
    """

    class Config:
        orm_mode = True

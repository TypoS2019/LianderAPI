#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.core.base_model import BaseModel


class ErrorResponseModel(BaseModel):
    detail: str         # error message

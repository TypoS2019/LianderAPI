#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Define an API version by making a selection of API routers"""

from fastapi import FastAPI

from app.routers.overige.overige_view import app as overige_router
from app.routers.interventie.interventie_view import app as interventie_router
from app.routers.gebeurtenis.gebeurtenis_view import app as gebeurtenis_router
from app.routers.gebruiker.gebruiker_view import app as gebruiker_router
from app.routers.project.project_view import app as project_router
from app.routers.scenario.scenario_view import app as scenario_router


app = FastAPI(title="Sample API", openapi_prefix='/api/v1/sample')

app.include_router(gebeurtenis_router, prefix='/gebeurtenis', tags=['gebeurtenis'])
app.include_router(gebruiker_router, prefix='/gebruiker', tags=['gebruiker'])
app.include_router(project_router, prefix='/project', tags=['project'])
app.include_router(overige_router, prefix='/overige', tags=['overige'])
app.include_router(interventie_router, prefix='/interventie', tags=['interventie'])
app.include_router(scenario_router, prefix='/scenario', tags=['scenario'])



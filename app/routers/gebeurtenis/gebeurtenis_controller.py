#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
from typing import List, Optional

from app.routers.gebeurtenis.gebeurtenis_models import GebeurtenisResponseModel
from app.routers.gebeurtenis.gebeurtenis_repository import GebeurtenisMapper


class GebeurtenisController(object):
    """Skeleton controller.

    Implements gebeurtenis related functionality.
    """

    """Initialiseert de gebeurtenismapper, om in de klasse te gebruiken"""

    def __init__(self):
        self.mapper = GebeurtenisMapper()

    """Stuurt de REST post-functie door naar de gebeurtenismapper, om een gebeurtenis toe te voegen"""

    def post_gebeurtenis(self, gebeurtenis: GebeurtenisResponseModel, project_id):
        self.mapper.add_gebeurtenis(gebeurtenis, project_id)
        return self.mapper.get_gebeurtenissen(project_id)

    """Stuurt de REST get-functie door naar de mapper om de gebeurtenissen op te halen"""

    def get_gebeurtenissen(self, project_id):
        return self.mapper.get_gebeurtenissen(project_id)

    """Stuurt de REST delete-functie door naar de mapper om de meegegeven gebeurtenis te verwijderen"""

    def delete_gebeurtenis(self, id: int, project_id):
        return self.mapper.delete_gebeurtenis(id, project_id)

    """Stuurt de REST update-functie door naar de mapper om de meegegeven gebeurtenis te updaten"""

    def update_gebeurtenis(self, model: GebeurtenisResponseModel, project_id):
        return self.mapper.update_gebeurtenis(model, project_id)

    '''voeg een gebeurtenis toe aan een scenario'''

    def add_interventie_to_gebeurtenis(self, gebeurtenis_id, interventie_id, project_id):
        self.mapper.add_interventie_to_gebeurtenis(gebeurtenis_id, interventie_id, project_id)

    """pas een waarde aan in gebeurtenis_interventie"""

    def update_interventie_in_gebeurtenis(self, gebeurtenis_id, interventie_id, waarde, project_id):
        self.mapper.update_interventie_in_gebeurtenis(gebeurtenis_id, interventie_id, waarde, project_id)

    '''remove gebeurtenis van scenario'''

    def remove_interventie_from_gebeurtenis(self, gebeurtenis_id, interventie_id, project_id):
        self.mapper.remove_interventie_from_gebeurtenis(gebeurtenis_id, interventie_id, project_id)

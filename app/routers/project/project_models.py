from typing import List

from app.core.base_model import BaseModel
import datetime

"""API request models, response models, and examples.
"""

"""Het ProjectResponseModel geeft weer welke informatie teruggegeven moet worden"""


class ProjectResponseModel(BaseModel):
    id: int = 1
    naam: str = "projectnaam"
    datum: datetime.date = datetime.date(2019, 12, 16)

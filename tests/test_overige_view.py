from unittest import TestCase
import mock
from fastapi import File
from starlette.responses import FileResponse
from starlette.testclient import TestClient
import pandas as pd

from app.routers.overige.overige_authentication_service import AuthenticationService
from app.routers.overige.overige_controller import OverigeController
from app.routers.overige.overige_models import OpslagResponseModel
from app.routers.overige.overige_view import app
from app.routers.scenario.scenario_controller import ScenarioController
from app.routers.gebeurtenis.gebeurtenis_controller import GebeurtenisController


class TestOverigeView(TestCase):
    test_value = {
        "scenarios": [
            {
                "id": 0,
                "naam": "string",
                "toelichting": "string",
                "result": {
                    "scenario_naam": "string",
                    "kosten_per_jaar": [
                        0
                    ]
                },
                "gebeurtenissen": [
                    {
                        "id": 0,
                        "Gebeurtenis": {
                            "id": 0,
                            "naam": "string",
                            "toelichting": "string",
                            "bronvermelding": "string",
                            "eenheid_per": "string",
                            "interventies": [
                                {
                                    "id": 0,
                                    "interventie": {
                                        "id": 0,
                                        "eenheid": "string",
                                        "naam": "string"
                                    },
                                    "waarde": 0
                                }
                            ]
                        },
                        "jaren": [
                            {
                                "waarde": 0,
                                "jaar": 0
                            }
                        ]
                    }
                ]
            }
        ],
        "gebeurtenissen": [
            {
                "id": 0,
                "naam": "string",
                "toelichting": "string",
                "bronvermelding": "string",
                "eenheid_per": "string",
                "interventies": [
                    {
                        "id": 0,
                        "interventie": {
                            "id": 0,
                            "eenheid": "string",
                            "naam": "string"
                        },
                        "waarde": 0
                    }
                ]
            }
        ],
        "interventies": [
            {
                "id": 0,
                "eenheid": "string",
                "naam": "string"
            }
        ]
    }

    """test_get_alle_data test of get_alle_data de correcte status code teruggeeft. """

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(OverigeController, 'collecteer_data', return_value=test_value)
    def test_get_alle_data(self, mock_collecteer_data, mocked_auth):
        client = TestClient(app)
        response = client.get('/opslaan?project_id=1')
        assert response.status_code == 200

    """test_get_alle_data_should_call_collecteer_data test of de juiste methode in de controller wordt aangeroepen. """

    @mock.patch.object(AuthenticationService, 'can_user_access', return_value=True)
    @mock.patch.object(OverigeController, 'collecteer_data', return_value=test_value)
    def test_get_alle_data_should_call_collecteer_data(self, mock_collecteer_data, mocked_auth):
        client = TestClient(app)
        response = client.get('/opslaan?project_id=1')
        mock_collecteer_data.assert_called()



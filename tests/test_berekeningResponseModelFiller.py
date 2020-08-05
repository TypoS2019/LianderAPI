from unittest import TestCase, mock

from app.routers.interventie.interventie_models import InterventieResponseModel
from app.routers.scenario.scenario_controller import BerekeningResponseModelFiller
from app.routers.scenario.scenario_models import InterventieMetWaardesPerJaar, GebeurtenisMetWaardesPerJaar, \
    BerekeningResponseModel
from app.routers.gebeurtenis.gebeurtenis_models import ScenarioGebeurtenisResponseModel, GebeurtenisResponseModel


def object_maker(type_model):
    model = None
    if type_model == "gebeurtenis":
        model = GebeurtenisMetWaardesPerJaar()
    elif type_model == "interventie":
        model = InterventieMetWaardesPerJaar()

    model.waardes_per_jaar = [0]
    return model


class TestBerekeningResponseModelFiller(TestCase):
    def setUp(self):
        self.sut = BerekeningResponseModelFiller()
        self.berekening_model = BerekeningResponseModel()
        self.scenario_gebeurtenis = ScenarioGebeurtenisResponseModel()
        self.scenario_gebeurtenis.Gebeurtenis = GebeurtenisResponseModel()
        self.interventie = InterventieResponseModel()

    @mock.patch.object(BerekeningResponseModelFiller, '_prepareer_nieuw_model',
                       return_value=object_maker("gebeurtenis"))
    def test_voeg_gebeurtenis_toe_aan_berekening_model_calls__prepareer_nieuw_model(self, mock__prepareer_nieuw_model):
        # Arrange

        # Act
        self.sut.voeg_gebeurtenis_toe_aan_berekening_model(self.berekening_model, 0, self.scenario_gebeurtenis, 0)

        # Assert
        mock__prepareer_nieuw_model.assert_called()

    @mock.patch.object(BerekeningResponseModelFiller, '_prepareer_nieuw_model',
                       return_value=object_maker("gebeurtenis"))
    def test_voeg_gebeurtenis_toe_aan_berekening_model_voegt_gegeven_waarde_toe(self, mock__prepareer_nieuw_model):
        # Arrange
        verwachtte_uitkomst = 10
        uitkomst_index = 0

        # Act
        self.sut.voeg_gebeurtenis_toe_aan_berekening_model(self.berekening_model, verwachtte_uitkomst,
                                                                    self.scenario_gebeurtenis, 0)
        output = self.berekening_model.gebeurtenis_met_waardes_per_jaar[0].waardes_per_jaar[uitkomst_index]

        # Assert
        assert output == verwachtte_uitkomst

    @mock.patch.object(BerekeningResponseModelFiller, '_prepareer_nieuw_model',
                       return_value=object_maker("interventie"))
    def test_voeg_interventie_toe_aan_berekening_model_calls__prepareer_nieuw_model(self, mock__prepareer_nieuw_model):
        # Arrange

        # Act
        self.sut.voeg_interventie_toe_aan_berekening_model(self.berekening_model, 0, self.interventie, 0)

        # Assert
        mock__prepareer_nieuw_model.assert_called()

    @mock.patch.object(BerekeningResponseModelFiller, '_prepareer_nieuw_model',
                       return_value=object_maker("interventie"))
    def test_voeg_gebeurtenis_toe_aan_berekening_model_voegt_gegeven_waarde_toe(self, mock__prepareer_nieuw_model):
        # Arrange
        verwachtte_uitkomst = 10
        uitkomst_index = 0

        # Act
        self.sut.voeg_interventie_toe_aan_berekening_model(self.berekening_model, verwachtte_uitkomst,
                                                           self.interventie, 0)
        output = self.berekening_model.interventie_met_waardes_per_jaar[0].waardes_per_jaar[uitkomst_index]

        # Assert
        assert output == verwachtte_uitkomst

    def test__prepareer_nieuw_model_maakt_gebeurtenis_model_als_daar_om_wordt_gevraagd(self):
        # Arrange

        # Act
        output = self.sut._prepareer_nieuw_model("gebeurtenis", "naam")

        # Assert
        assert output.__class__ == GebeurtenisMetWaardesPerJaar().__class__

    def test__prepareer_nieuw_model_maakt_interventie_model_als_daar_om_wordt_gevraagd(self):
        # Arrange

        # Act
        output = self.sut._prepareer_nieuw_model("interventie", "naam")

        # Assert
        assert output.__class__ == InterventieMetWaardesPerJaar().__class__

    def test__prepareer_nieuw_model_maakt_een_array_met_een_lengte_van_honderd(self):
        # Arrange
        verwachtte_lengte = 100

        # Act
        output = self.sut._prepareer_nieuw_model("gebeurtenis", "naam")

        # Assert
        assert len(output.waardes_per_jaar) == verwachtte_lengte

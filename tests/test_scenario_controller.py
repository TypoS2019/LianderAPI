from unittest import TestCase
from unittest.mock import patch

import mock

from app.routers.interventie.interventie_models import GebeurtenisInterventieResponseModel, InterventieResponseModel
from app.routers.scenario.scenario_controller import ScenarioController
from app.routers.scenario.scenario_controller import LCVCalculator
from app.routers.scenario.scenario_models import ScenarioResponseModel
from app.routers.scenario.scenario_repository import ScenarioMapper
from app.routers.gebeurtenis.gebeurtenis_models import ScenarioGebeurtenisResponseModel, GebeurtenisResponseModel, \
    WaardePerJaar


class TestScenarioController(TestCase):

    def setUp(self):
        self.sut = ScenarioController()
        self.wacc = 5
        self.jaren = 100

    '''Maakt een lijst met een enkel scenario om test mee uit te voeren'''
    def _scenario_lijst_maker(self, scenario_id):
        scenario = ScenarioResponseModel()
        scenario.id = scenario_id
        scenario.naam = 'naam'
        scenario.toelichting = 't'
        scenario.result = None
        '''Voeg scenario toe'''
        sg = ScenarioGebeurtenisResponseModel()
        sg.id = 0
        gebeurtenis = GebeurtenisResponseModel()
        gebeurtenis.id = 0
        gebeurtenis.naam = 'gebeurtenis'
        gi = GebeurtenisInterventieResponseModel()
        gi.waarde = 20
        '''Voeg interventie toe'''
        interventie = InterventieResponseModel()
        interventie.waarde = 1
        interventie.type = "w"
        gi.interventie = interventie
        '''voeg jaren toe'''
        gebeurtenis.interventies = [gi]
        sg.Gebeurtenis = gebeurtenis
        jaar = WaardePerJaar()
        jaar.waarde = 2
        jaar.jaar = 0
        jaar2 = WaardePerJaar()
        jaar2.waarde = 1
        jaar2.jaar = 1
        sg.jaren = [jaar, jaar2]
        scenario.gebeurtenissen = [sg]

        return [scenario]

    """test_get_scenario_calls_correct_method_from_repository test of de  juiste methode wordt aangeroepen. """

    @mock.patch.object(ScenarioMapper, 'get_scenarios', return_value=[])
    def test_get_scenario_calls_correct_method_from_repository(self, mock_get_scenarios):
        self.sut.get_all_scenarios(1)
        mock_get_scenarios.assert_called_with(1)

    """test_delete_scenario_calls_correct_method_from_repository test of de  juiste methode wordt aangeroepen. """

    @mock.patch.object(ScenarioMapper, 'delete_scenario', return_value=[])
    def test_delete_scenario_calls_correct_method_from_repository(self, mock_delete_scenario):
        self.sut.delete_scenario(1, 1)
        mock_delete_scenario.assert_called_with(1, 1)

    """test_update_scenario_calls_correct_method_from_repository test of de  juiste methode wordt aangeroepen. """

    @mock.patch.object(ScenarioMapper, 'update_scenario', return_value=[])
    def test_update_scenario_calls_correct_method_from_repository(self, mock_update_scenario):
        self.sut.update_scenario(ScenarioResponseModel, 1)
        mock_update_scenario.assert_called_with(ScenarioResponseModel, 1)

    """test_add_scenario_calls_correct_method_from_repository test of de  methode vreate_scenario in de 
        controller correct werkt. """

    @mock.patch.object(ScenarioMapper, 'add_scenario', return_value=[])
    def test_add_scenario_calls_correct_method_from_repository(self, mock_add_scenario):
        self.sut.create_scenario(ScenarioResponseModel, 1)
        mock_add_scenario.assert_called_with(
            ScenarioResponseModel, 1)  # check of add_gebeurtenis in de repository wordt aangeroepen

    @mock.patch.object(ScenarioMapper, 'get_scenarios', return_value=[])
    def test_get_scenario_from_id_calls_correct_method_from_repository(self, mock_get_scenarios):
        self.sut.get_scenario_from_id(1, 1)
        mock_get_scenarios.assert_called_with(1)

    @mock.patch.object(ScenarioMapper, 'get_scenarios', return_value=[])
    def test_get_multiple_scenarios_from_ids_calls_correct_method_from_repository(self, mock_get_scenarios):
        self.sut.get_multiple_scenarios_from_ids(1, [1])
        mock_get_scenarios.assert_called_with(1)

    @mock.patch.object(ScenarioController, '_is_id_gelijk', return_value=True)
    @mock.patch.object(ScenarioMapper, 'get_scenarios', return_value=_scenario_lijst_maker(object, 1))
    @mock.patch.object(LCVCalculator, 'bereken_lcv_voor_scenario', return_value=[1])
    def test_get_scenario_from_id_returns_scenario_with_id_one(self, mock__is_id_gelijk, mock_get_scenarios,
                                                               mock_bereken_lcv_voor_scenario):
        # Arrange
        verwachtte_id = 1

        # Act
        output = self.sut.get_scenario_from_id(1, verwachtte_id)
        daadwerkelijke_id = output.id

        # Assert
        assert verwachtte_id == daadwerkelijke_id

    @mock.patch.object(ScenarioController, '_is_id_gelijk', return_value=True)
    @mock.patch.object(ScenarioMapper, 'get_scenarios', return_value=_scenario_lijst_maker(object, 1))
    @mock.patch.object(LCVCalculator, 'bereken_lcv_voor_scenario', return_value=[1])
    def test_get_multiple_scenarios_by_ids_returns_scenario_with_id_one(self, mock__is_id_gelijk, mock_get_scenarios,
                                                               mock_bereken_lcv_voor_scenario):
        # Arrange
        verwachtte_id = [1]

        # Act
        output = self.sut.get_multiple_scenarios_from_ids(1, verwachtte_id)
        daadwerkelijke_id = output[0].id

        # Assert
        assert verwachtte_id[0] == daadwerkelijke_id

    def test__is_id_gelijk(self):
        # Arrange
        scenario_id = 1
        opgegeven_id = 1
        verwachtte_boolean = True

        # Act
        output = self.sut._is_id_gelijk(scenario_id, opgegeven_id)

        # Assert
        assert output == verwachtte_boolean

    @mock.patch.object(ScenarioMapper, 'add_gebeurtenis_to_scenario', return_value=[])
    def test_add_gebeurtenis_to_scenario(self, mock_add_gebeurtenis_to_scenario):
        scenario_id = 1
        gebeurtenis_id = 2
        self.sut.add_gebeurtenis_to_scenario(scenario_id, gebeurtenis_id, 1)
        mock_add_gebeurtenis_to_scenario.assert_called_with(scenario_id, gebeurtenis_id, 1)

    @mock.patch.object(ScenarioMapper, 'remove_gebeurtenis_from_scenario', return_value=[])
    def test_remove_gebeurtenis_from_scenario(self, mock_remove_gebeurtenis_from_scenario):
        scenario_id = 1
        gebeurtenis_id = 2
        self.sut.remove_gebeurtenis_from_scenario(scenario_id, gebeurtenis_id, 1)
        mock_remove_gebeurtenis_from_scenario.assert_called_with(scenario_id, gebeurtenis_id, 1)

    @mock.patch.object(ScenarioMapper, 'add_jaar_to_gebeurtenis_in_scenario', return_value=[])
    def test_add_jaar(self, mock_add_jaar_to_gebeurtenis_in_scenario):
        scenario_id = 1
        gebeurtenis_id = 2
        jaar = 3
        waarde = 4
        self.sut.add_jaar_to_gebeurtenis_in_scenario(scenario_id, gebeurtenis_id, jaar, waarde, 1)
        mock_add_jaar_to_gebeurtenis_in_scenario.assert_called_with(scenario_id, gebeurtenis_id, jaar, waarde, 1)

    @mock.patch.object(ScenarioMapper, 'update_jaar_in_gebeurtenis_in_scenario', return_value=[])
    def test_update_jaar(self, mock_update_jaar_in_gebeurtenis_in_scenario):
        scenario_id = 1
        gebeurtenis_id = 2
        jaar = 3
        waarde = 4
        self.sut.update_jaar_in_gebeurtenis_in_scenario(scenario_id, gebeurtenis_id, jaar, waarde, 1)
        mock_update_jaar_in_gebeurtenis_in_scenario.assert_called_with(scenario_id, gebeurtenis_id, jaar, waarde, 1)

    @mock.patch.object(ScenarioMapper, 'remove_jaar_from_gebeurtenis', return_value=[])
    def test_remove_jaar(self, mock_remove_jaar_from_gebeurtenis):
        scenario_id = 1
        gebeurtenis_id = 2
        jaar = 3
        self.sut.remove_jaar_from_gebeurtenis_in_scenario(scenario_id, gebeurtenis_id, jaar, 1)
        mock_remove_jaar_from_gebeurtenis.assert_called_with(scenario_id, gebeurtenis_id, jaar, 1)

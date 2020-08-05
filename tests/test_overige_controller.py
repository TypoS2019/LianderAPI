from unittest import TestCase

import mock
from fastapi import File
from pandas import DataFrame

from app.routers.gebeurtenis.gebeurtenis_models import GebeurtenisResponseModel
from app.routers.gebeurtenis.gebeurtenis_repository import GebeurtenisMapper
from app.routers.interventie.interventie_models import InterventieResponseModel
from app.routers.overige.overige_controller import OverigeController
from app.routers.scenario.scenario_controller import ScenarioController, LCVCalculator
from app.routers.scenario.scenario_models import BerekeningResponseModel, ScenarioResponseModel
from app.routers.gebeurtenis.gebeurtenis_controller import GebeurtenisController
from app.routers.scenario.scenario_repository import ScenarioMapper


class TestOverigeController(TestCase):

    def setUp(self):
        self.overige_controller = OverigeController()

    """test_get_gebeurtenissen_calls_correct_method_from_repository test of de  juiste methodes in de 
    ScenarioController en GebeurtenisController worden aangeroepen. """

    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[])
    @mock.patch.object(GebeurtenisController, 'get_gebeurtenissen', return_value=[])
    def test_get_gebeurtenissen_calls_correct_method_from_repository(self, mock_get_all_scenarios,
                                                                     mock_get_gebeurtenissen):
        project_id = 1

        self.overige_controller.collecteer_data(project_id)
        mock_get_all_scenarios.assert_called_with(project_id)
        mock_get_gebeurtenissen.assert_called_with(project_id)

    """Deze test checkt of collecteer_resultaten de functie bereken_lcv_voor_scenario van LCVCalculator aanroept"""

    @mock.patch.object(LCVCalculator, 'bereken_lcv_voor_scenario', return_value=BerekeningResponseModel())
    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[ScenarioResponseModel()])
    def test_collecteer_resultaten_calls_lcv_calculator_bereken_lcv_voor_scenario(self, mock_bereken_lcv_voor_scenario,
                                                                                  mock_get_all_scenarios):
        # Arrange
        project_id = 1

        # Act
        self.overige_controller.collecteer_resultaten(project_id)

        # Assert
        mock_bereken_lcv_voor_scenario.assert_called_with(project_id)

    """Deze test checkt of collecteer_resultaten de functie get_all_scenarios ScenarioController"""

    @mock.patch.object(ScenarioController, 'get_all_scenarios', return_value=[ScenarioResponseModel()])
    @mock.patch.object(LCVCalculator, 'bereken_lcv_voor_scenario', return_value=BerekeningResponseModel())
    def test_collecteer_resultaten_calls_scenario_controller_get_all_scenarios(self, mock_bereken_lcv_voor_scenario,
                                                                               mock_get_all_scenarios):
        # Arrange
        project_id = 1

        # Act
        self.overige_controller.collecteer_resultaten(project_id)

        # Assert
        mock_get_all_scenarios.assert_called_with(project_id)

    """test_collecteer_resultaten_voor_scenario_calls_method_from_scenario_controller test of de methode in de 
    scenarioController wordt aangeroepen"""

    @mock.patch.object(LCVCalculator, 'bereken_lcv_voor_scenario', return_value=BerekeningResponseModel())
    @mock.patch.object(ScenarioController, 'get_scenario_from_id', return_value=ScenarioResponseModel())
    def test_collecteer_resultaten_voor_scenario_calls_method_from_scenario_controller(self, mock_get_scenario_from_id,
                                                                                       mock_bereken_lcv_voor_scenario):
        test_id = 1
        project_id = 1
        self.overige_controller.collecteer_resultaten_voor_scenario(project_id, test_id)
        mock_get_scenario_from_id.assert_called_with(project_id, test_id)

    """test_collecteer_resultaten_voor_scenario_calls_method_from_lcv_calculator test of de methode in de lcvCalculator 
    wordt aangeroepen"""

    @mock.patch.object(LCVCalculator, 'bereken_lcv_voor_scenario', return_value=BerekeningResponseModel())
    @mock.patch.object(ScenarioController, 'get_scenario_from_id', return_value=ScenarioResponseModel())
    def test_collecteer_resultaten_voor_scenario_calls_method_from_lcv_calculator(self, mock_get_scenario_from_id,
                                                                                  mock_bereken_lcv_voor_scenario):
        test_id = 1
        project_id = 1
        test_model = ScenarioResponseModel()
        test_jaren = 100
        self.overige_controller.collecteer_resultaten_voor_scenario(project_id, test_id)
        mock_bereken_lcv_voor_scenario.assert_called_with(test_model, test_jaren)

    """test_get_excel_calls_method_collecteer_resultaten_voor_scenario test of collecteer_resultaten_voor_scenario 
    wordt aangeroepen"""

    @mock.patch.object(OverigeController, '_get_alle_jaren', return_value=[])
    @mock.patch.object(OverigeController, '_get_lcv_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_lcc_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_waardering_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_sum', return_value=1)
    @mock.patch.object(OverigeController, 'collecteer_resultaten_voor_scenario', return_value=BerekeningResponseModel())
    def test_get_excel_calls_method_collecteer_resultaten_voor_scenario(self, mock_collecteer_resultaten_voor_scenario,
                                                                        mock_get_alle_jaren, mock_get_lcv_lijst,
                                                                        mock_get_lcc_lijst, mock_get_waardering_lijst,
                                                                        mock_get_sum):
        test_id = 1
        project_id = 1
        start_jaar = 100
        self.overige_controller.get_excel(project_id, test_id)
        mock_collecteer_resultaten_voor_scenario.assert_called_with(project_id, test_id)

    """test_get_excel_calls_method_get__alle_jaren test of _get_alle_jaren wordt aangeroepen"""

    @mock.patch.object(OverigeController, '_get_lcv_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_lcc_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_waardering_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_sum', return_value=1)
    @mock.patch.object(OverigeController, 'collecteer_resultaten_voor_scenario', return_value=BerekeningResponseModel())
    @mock.patch.object(OverigeController, '_get_alle_jaren', return_value=[])
    def test_get_excel_calls_method_get__alle_jaren(self, mock_get_alle_jaren, mock_collecteer_resultaten_voor_scenario,
                                                    mock_get_lcv_lijst, mock_get_lcc_lijst, mock_get_waardering_lijst,
                                                    mock_get_sum):
        test_id = 1
        project_id = 1
        test_aantal_jaren = 100
        test_startjaar = 2020
        self.overige_controller.get_excel(project_id, test_id)
        mock_get_alle_jaren.assert_called_with(test_startjaar, test_aantal_jaren)

    """test_get_excel_calls_method_get__get_lcv_lijst test of _get_lcv_lijst wordt aangeroepen"""

    @mock.patch.object(OverigeController, '_get_lcc_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_waardering_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_sum', return_value=1)
    @mock.patch.object(OverigeController, 'collecteer_resultaten_voor_scenario', return_value=BerekeningResponseModel())
    @mock.patch.object(OverigeController, '_get_alle_jaren', return_value=[])
    @mock.patch.object(OverigeController, '_get_lcv_lijst', return_value=[])
    def test_get_excel_calls_method_get__get_lcv_lijst(self, mock_get_lcv_lijst, mock_get_alle_jaren,
                                                       mock_collecteer_resultaten_voor_scenario, mock_get_lcc_lijst,
                                                       mock_get_waardering_lijst, mock_get_sum):
        test_id = 1
        project_id = 1
        test_aantal_jaren = 100
        test_model = BerekeningResponseModel()
        self.overige_controller.get_excel(project_id, test_id)
        mock_get_lcv_lijst.assert_called_with(test_model, test_aantal_jaren)

    """test_get_excel_calls_method_get__get_lcv_lijst test of _get_lcc_lijst wordt aangeroepen"""

    @mock.patch.object(OverigeController, '_get_waardering_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_sum', return_value=1)
    @mock.patch.object(OverigeController, 'collecteer_resultaten_voor_scenario', return_value=BerekeningResponseModel())
    @mock.patch.object(OverigeController, '_get_alle_jaren', return_value=[])
    @mock.patch.object(OverigeController, '_get_lcv_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_lcc_lijst', return_value=[])
    def test_get_excel_calls_method_get__get_lcc_lijst(self, mock_get_lcc_lijst, mock_get_lcv_lijst,
                                                       mock_get_alle_jaren, mock_collecteer_resultaten_voor_scenario,
                                                       mock_get_waardering_lijst, mock_get_sum):
        test_id = 1
        project_id = 1
        test_aantal_jaren = 100
        test_model = BerekeningResponseModel()
        self.overige_controller.get_excel(project_id, test_id)
        mock_get_lcc_lijst.assert_called_with(test_model, test_aantal_jaren)

    """test_get_excel_calls_method_get__get_waardering_lijst test of _get_waardering_lijst wordt aangeroepen"""

    @mock.patch.object(OverigeController, '_get_sum', return_value=1)
    @mock.patch.object(OverigeController, 'collecteer_resultaten_voor_scenario', return_value=BerekeningResponseModel())
    @mock.patch.object(OverigeController, '_get_alle_jaren', return_value=[])
    @mock.patch.object(OverigeController, '_get_lcv_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_lcc_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_waardering_lijst', return_value=[])
    def test_get_excel_calls_method_get__get_waardering_lijst(self, mock_get_waardering_lijst, mock_get_lcc_lijst,
                                                              mock_get_lcv_lijst, mock_get_alle_jaren,
                                                              mock_collecteer_resultaten_voor_scenario, mock_get_sum):
        test_id = 1
        project_id = 1
        test_aantal_jaren = 100
        test_model = BerekeningResponseModel()
        self.overige_controller.get_excel(project_id, test_id)
        mock_get_waardering_lijst.assert_called_with(test_model, test_aantal_jaren)

    """test_get_excel_calls_method_get__get_sum test of _get_sum wordt aangeroepen"""

    @mock.patch.object(OverigeController, 'collecteer_resultaten_voor_scenario', return_value=BerekeningResponseModel())
    @mock.patch.object(OverigeController, '_get_alle_jaren', return_value=[])
    @mock.patch.object(OverigeController, '_get_lcv_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_lcc_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_waardering_lijst', return_value=[])
    @mock.patch.object(OverigeController, '_get_sum', return_value=1)
    def test_get_excel_calls_method_get__get_sum(self, mock_get_sum, mock_get_waardering_lijst,
                                                 mock_get_lcc_lijst, mock_get_lcv_lijst,
                                                 mock_get_alle_jaren,
                                                 mock_collecteer_resultaten_voor_scenario):
        test_id = 1
        project_id = 1
        test_waardes = [1]
        self.overige_controller.get_excel(project_id, test_id)
        mock_get_sum.assert_called_with(test_waardes)

    """test__schrijf_dataframe_naar_excel test of _random_name_generator wordt aangeroepen"""

    @mock.patch.object(OverigeController, '_random_name_generator', return_value=123456789)
    def test__schrijf_dataframe_naar_excel_calls_method__random_name_generator(self, mock__random_name_generator):
        test_df = DataFrame()
        self.overige_controller._schrijf_dataframe_naar_excel(test_df, test_df)
        mock__random_name_generator.assert_called_with()

    """test__get_alle_jaren test of _get_alle_jaren de juiste waarde teruggeeft"""
    def test__get_alle_jaren(self):
        test_aantal_jaren = 0
        test_startjaar = 2019
        assert self.overige_controller._get_alle_jaren(test_startjaar, test_aantal_jaren) == []

    """test__get_lcv_lijst test of _get_lcv_lijst de juiste waarde teruggeeft"""
    def test__get_lcv_lijst(self):
        test_model = BerekeningResponseModel()
        test_aantal_jaren = 0
        assert self.overige_controller._get_lcv_lijst(test_model, test_aantal_jaren) == []

    """test__get_lcc_lijst test of _get_lcc_lijst de juiste waarde teruggeeft"""
    def test__get_lcc_lijst(self):
        test_model = BerekeningResponseModel()
        test_aantal_jaren = 0
        assert self.overige_controller._get_lcc_lijst(test_model, test_aantal_jaren) == []

    """test__get_waardering_lijst test of _get_waardering_lijst de juiste waarde teruggeeft"""
    def test__get_waardering_lijst(self):
        test_model = BerekeningResponseModel()
        test_aantal_jaren = 0
        assert self.overige_controller._get_waardering_lijst(test_model, test_aantal_jaren) == []

    """test__get_sum test of _get_sum de juiste waarde teruggeeft"""
    def test__get_sum(self):
        test_waardes = [1, 2]
        assert self.overige_controller._get_sum(test_waardes) == 3

    """"test_get_all_excel_sheet_names uitlezen van excel bestand op verschillende sheet namen"""
    # def test_get_all_excel_sheet_names(self):
    #     mocked_file = 'Mocked_excel.xlsx'
    #     assert self.overige_controller.get_all_excel_sheet_names(mocked_file) == ['Gebeurtenis', 'Interventie', 'Scenario']

    """test_convert_excel_sheet_to_json testen of excel bestand gelezen kan worden en omgezet naar Json"""
    # def test_convert_excel_sheet_to_json(self):
    #     mocked_file = 'Mocked_excel.xlsx'
    #     return_json = {'Eenheid_interventie': {'0': '€',
    #                                            '1': '€',
    #                                            '2': '€eq',
    #                                            '3': 'ton CO2 eq',
    #                                            '4': '€',
    #                                            '5': '€',
    #                                            '6': '€',
    #                                            '7': '€',
    #                                            '8': '€',
    #                                            '9': '€'},
    #                    'Naam_interventie': {'0': 'CAPEX',
    #                                         '1': 'OPEX',
    #                                         '2': 'Waardering',
    #                                         '3': 'CO2-Uitstoot',
    #                                         '4': 'Geert',
    #                                         '5': 'Steppe',
    #                                         '6': 'Romy',
    #                                         '7': 'Luc',
    #                                         '8': 'Daniel',
    #                                         '9': 'test_data'},
    #                    'Toelichting_interventie': {'0': 'Capital Expenditure (investeringen)',
    #                                                '1': 'Operational Expenditure (operationele '
    #                                                     'kosten)',
    #                                                '2': 'Iets waarderen met geldwaarde',
    #                                                '3': 'Milleuschade door emissies van CO2 in '
    #                                                     'atmosfeer',
    #                                                '4': 'lid 1',
    #                                                '5': 'lid 2',
    #                                                '6': 'lid 3',
    #                                                '7': 'lid 4',
    #                                                '8': 'lid 5',
    #                                                '9': 'test_data'},
    #                    'Type_interventie': {'0': 'c',
    #                                         '1': 'c',
    #                                         '2': 'w',
    #                                         '3': 'w',
    #                                         '4': 'c',
    #                                         '5': 'w',
    #                                         '6': 'w',
    #                                         '7': 'c',
    #                                         '8': 'c',
    #                                         '9': 'c'},
    #                    'Waarde_interventie': {'0': 1.0,
    #                                           '1': 1.0,
    #                                           '2': 1.0,
    #                                           '3': 0.11,
    #                                           '4': 1.0,
    #                                           '5': 2.0,
    #                                           '6': 3.0,
    #                                           '7': 4.0,
    #                                           '8': 5.0,
    #                                           '9': 8.0}}
    #     assert self.overige_controller.convert_excel_sheet_to_json(mocked_file, sheet_name='Interventie') == return_json

    """test_json_model_array_gebeurtenis testen of Json in een gebeurtenis model array gezet is"""
    def test_json_model_array_gebeurtenis(self):
        json_model_array = []
        data_json = {'Bron_gebeurtenis': {'0': 'Bronvermelding gebeurtenis',
                      '1': 'Bronvermelding gebeurtenis',
                      '2': 'Bronvermelding gebeurtenis',
                      '3': 'Bronvermelding gebeurtenis',
                      '4': 'Bronvermelding gebeurtenis',
                      '5': 'Bronvermelding gebeurtenis',
                      '6': 'Bronvermelding gebeurtenis',
                      '7': 'Bronvermelding gebeurtenis',
                      '8': 'Bronvermelding gebeurtenis'},
                     'Eenheid_gebeurtenis': {'0': 'stuk',
                                             '1': 'stuk',
                                             '2': 'stuk',
                                             '3': 'stuk',
                                             '4': 'stuk',
                                             '5': 'stuk',
                                             '6': 'stuk',
                                             '7': 'BLA',
                                             '8': 'test_data'},
                     'Naam_gebeurtenis': {'0': 'Aanschaf Edison 70D',
                                          '1': 'Aanschaf Nippon Green',
                                          '2': 'Aanschaf WV Cricket benzine',
                                          '3': 'Aanschaf WV Cricket diesel',
                                          '4': 'Geert-Jan',
                                          '5': 'Romy',
                                          '6': 'Luc',
                                          '7': 'BLABLABLA',
                                          '8': 'test_data'},
                     'Toelichting_gebeurtenis': {'0': 'Luxe elektrische auto (sedan)',
                                                 '1': 'Compacte Elektrische auto (hatchback)',
                                                 '2': 'Compacte benzine auto (hatchback)',
                                                 '3': 'Compacte diesel auto (hatchback)',
                                                 '4': 'Mitch',
                                                 '5': 'Steppe',
                                                 '6': 'Daniel',
                                                 '7': 'BLABLA',
                                                 '8': 'test_data'}}
        for i in range(len(data_json["Naam_gebeurtenis"])):
            model = GebeurtenisResponseModel()
            model.id = i
            model.naam = data_json["Naam_gebeurtenis"][str(i)]
            model.toelichting = data_json["Toelichting_gebeurtenis"][str(i)]
            model.bronvermelding = data_json["Bron_gebeurtenis"][str(i)]
            model.eenheid_per = data_json["Eenheid_gebeurtenis"][str(i)]
            json_model_array.append(model)
        assert self.overige_controller.json_model_array_gebeurtenis(data_json) == json_model_array

    """test_json_model_array_interventie testen of Json in een interventie model array gezet is"""
    def test_json_model_array_interventie(self):
        json_model_array = []
        data_json = {'Eenheid_interventie': {'0': '€',
                                               '1': '€',
                                               '2': '€eq',
                                               '3': 'ton CO2 eq',
                                               '4': '€',
                                               '5': '€',
                                               '6': '€',
                                               '7': '€',
                                               '8': '€',
                                               '9': '€'},
                       'Naam_interventie': {'0': 'CAPEX',
                                            '1': 'OPEX',
                                            '2': 'Waardering',
                                            '3': 'CO2-Uitstoot',
                                            '4': 'Geert',
                                            '5': 'Steppe',
                                            '6': 'Romy',
                                            '7': 'Luc',
                                            '8': 'Daniel',
                                            '9': 'test_data'},
                       'Toelichting_interventie': {'0': 'Capital Expenditure (investeringen)',
                                                   '1': 'Operational Expenditure (operationele '
                                                        'kosten)',
                                                   '2': 'Iets waarderen met geldwaarde',
                                                   '3': 'Milleuschade door emissies van CO2 in '
                                                        'atmosfeer',
                                                   '4': 'lid 1',
                                                   '5': 'lid 2',
                                                   '6': 'lid 3',
                                                   '7': 'lid 4',
                                                   '8': 'lid 5',
                                                   '9': 'test_data'},
                       'Type_interventie': {'0': 'c',
                                            '1': 'c',
                                            '2': 'w',
                                            '3': 'w',
                                            '4': 'c',
                                            '5': 'w',
                                            '6': 'w',
                                            '7': 'c',
                                            '8': 'c',
                                            '9': 'c'},
                       'Waarde_interventie': {'0': 1.0,
                                              '1': 1.0,
                                              '2': 1.0,
                                              '3': 0.11,
                                              '4': 1.0,
                                              '5': 2.0,
                                              '6': 3.0,
                                              '7': 4.0,
                                              '8': 5.0,
                                              '9': 8.0}}
        for i in range(len(data_json["Naam_interventie"])):
            model = InterventieResponseModel()
            model.id = i
            model.naam = data_json["Naam_interventie"][str(i)]
            model.type = data_json["Type_interventie"][str(i)]
            model.eenheid = data_json["Eenheid_interventie"][str(i)]
            model.waarde = data_json["Waarde_interventie"][str(i)]
            model.toelichting = data_json["Toelichting_interventie"][str(i)]
            json_model_array.append(model)
        assert self.overige_controller.json_model_array_interventie(data_json) == json_model_array

    """test_json_model_array_scenario testen of Json in een scenario model array gezet is"""
    def test_json_model_array_scenario(self):
        json_model_array = []
        data_json = {'Naam_scenario': {'0': 'Edison 70D',
                   '1': 'Nippon Green',
                   '2': 'WV Cricket Benzine',
                   '3': 'WV Cricket Diesel',
                   '4': 'Donut',
                   '5': 'Pizza',
                   '6': 'Cheescake',
                   '7': 'test_data'},
                     'Toelichting_scenario': {'0': "Scenario toelichting",
                                              '1': "Scenario toelichting",
                                              '2': "Scenario toelichting",
                                              '3': "Scenario toelichting",
                                              '4': "Scenario toelichting",
                                              '5': "Scenario toelichting",
                                              '6': "Scenario toelichting",
                                              '7': 'test_data'}}
        for i in range(len(data_json["Naam_scenario"])):
            model = ScenarioResponseModel()
            model.id = i
            model.naam = data_json["Naam_scenario"][str(i)]
            model.toelichting = data_json["Toelichting_scenario"][str(i)]
            json_model_array.append(model)
        assert self.overige_controller.json_model_array_scenario(data_json) == json_model_array



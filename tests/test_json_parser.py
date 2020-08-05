from unittest import TestCase

from app.routers.overige.overige_repository import JSONParser


class TestJsonParser(TestCase):
    def test_genereer_jaar(self):
        jaar_waarde = 10
        row = (1, 'Edison 70D', '', 1, 19, 6, 6, 8, jaar_waarde, 19, 'Nieuwe banden (sedan)',
               'Vervangen van banden na 60.000 Km', '', 'stuk', 19, 1, 100.0, 1, 'CAPEX', 'c', '€', 1.0,
               'Capital Expenditure (investeringen)')

        parser = JSONParser()

        jaar = parser._genereer_jaar(row, 0)

        assert jaar.waarde == jaar_waarde

    def test_genereer_interventie(self):
        naam = "CAPEX"
        row = (
        1, 'Edison 70D', '', 1, 19, 6, 6, 8, 8, 19, 'Nieuwe banden (sedan)', 'Vervangen van banden na 60.000 Km', '',
        'stuk', 19, 1, 100.0, 1, naam, 'c', '€', 1.0, 'Capital Expenditure (investeringen)')

        parser = JSONParser()

        interventie = parser._genereer_interventie(row, 0, 0)

        assert interventie.interventie.naam == naam

    def test_genereer_gebeurtenis(self):
        naam = "Nieuwe banden (sedan)"
        row = (
            1, 'Edison 70D', '', 1, 19, 6, 6, 8, 8, 19, naam, 'Vervangen van banden na 60.000 Km',
            '',
            'stuk', 19, 1, 100.0, 1, 'CAPEX', 'c', '€', 1.0, 'Capital Expenditure (investeringen)')

        parser = JSONParser()

        gebeurtenis = parser._genereer_gebeurtenis([], row, 0, [], 0)

        assert gebeurtenis.naam == naam

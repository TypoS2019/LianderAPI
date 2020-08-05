INSERT INTO Interventie (naam, type, eenheid, waarde, toelichting)
VALUES ('CAPEX', 'c', '€', 1, 'Capital Expenditure (investeringen)'),
       ('OPEX', 'c', '€', 1, 'Operational Expenditure (operationele kosten)'),
       ('Waardering', 'w', '€eq.', 1, 'Iets waarderen met geldwaarde'),
       ('CO2-Uitstoot', 'w', 'ton CO2 eq.', 0.11, 'Milleuschade door emissies van CO2 in atmosfeer');

INSERT INTO gebeurtenis (naam, toelichting, bron, eenheid)
VALUES ('Aanschaf Edison 70D', 'Luxe elektrische auto (sedan)', '', 'stuk'),
       ('Aanschaf Nippon Green', 'Compacte Elektrische auto (hatchback)', '', 'stuk'),
       ('Aanschaf WV Cricket benzine', 'Compacte benzine auto (hatchback)', '', 'stuk'),
       ('Aanschaf WV Cricket diesel', 'Compacte diesel auto (hatchback)', '', 'stuk'),
       ('Verbruik elektriciteit', 'Laden accu', '', 'kWh'),
       ('Verbruik Benzine', 'Tanken benzine', '', 'liter'),
       ('Verbruik Diesel', 'Tanken diesel', '', 'liter'),
       ('Wegenbelasting WV Cricket benzine', '', '', 'jaar'),
       ('Wegenbelasting WV Cricket diesel', '', '', 'jaar'),
       ('Verzekering Edison 70D (WA)', 'Alleen WA', '', 'maand'),
       ('Verzekering Edison 70D (Allrisk)', 'Allrisk', '', 'maand'),
       ('Verzekering Nippon Green (WA)', 'Alleen WA', '', 'maand'),
       ('Verzekering Nippon Green (Allrisk)', 'Allrisk', '', 'maand'),
       ('Verzekering WV Cricket benzine (WA)', 'Alleen WA', '', 'maand'),
       ('Verzekering WV Cricket benzine (Allrisk)', 'Allrisk', '', 'maand'),
       ('Verzekering WV Cricket diesel (WA)', 'Alleen WA', '', 'maand'),
       ('Verzekering WV Cricket diesel (Allrisk)', 'Allrisk', '', 'maand'),
       ('Nieuwe banden (hatchback)', 'Vervangen van banden na 60.000 Km', '', 'stuk'),
       ('Nieuwe banden (sedan)', 'Vervangen van banden na 60.000 Km', '', 'stuk'),
       ('Bandenwissel', 'Wisselen zomer & winterbanden', '', 'keer'),
       ('APK keuring', 'Verplichte jaarlijkse keuring', '', 'keer'),
       ('Kleine beurt hatchback', 'Klein onderhoud elke 20.000 Km', '', 'keer'),
       ('Kleine beurt sedan', 'Klein onderhoud elke 20.000 Km', '', 'keer'),
       ('Grote beurt hatchback', 'Groot onderhoud', '', 'keer'),
       ('Grote beurt sedan', 'Groot onderhoud', '', 'keer'),
       ('Verkoop van Edison 70D', 'Restwaarde bij verkoop als tweedehands auto', '', 'keer'),
       ('Verkoop van Nippon Green', 'Restwaarde bij verkoop als tweedehands auto', '', 'keer'),
       ('Verkoop van WV Cricket benzine', 'Restwaarde bij verkoop als tweedehands auto', '', 'keer'),
       ('Verkoop van WV Cricket diesel', 'Restwaarde bij verkoop als tweedehands auto', '', 'keer');

INSERT INTO scenario (naam, toelichting)
VALUES ('Edison 70D', ''),
       ('Nippon Green', ''),
       ('WV Cricket Benzine', ''),
       ('WV Cricket Diesel', '');

INSERT INTO gebeurtenis_interventie (gebeurtenis_id, interventie_id, waarde)
VALUES #Aanschaf Edison 70D
       ((SELECT id FROM gebeurtenis WHERE naam = 'Aanschaf Edison 70D'),
        (SELECT id FROM interventie WHERE naam = 'CAPEX'), 90000),
       ((SELECT id FROM gebeurtenis WHERE naam = 'Aanschaf Edison 70D'),
        (SELECT id FROM interventie WHERE naam = 'CO2-Uitstoot'), 17000),
       #Aanschaf Nippon Green
       ((SELECT id FROM gebeurtenis WHERE naam = 'Aanschaf Nippon Green'),
        (SELECT id FROM interventie WHERE naam = 'CAPEX'), 38000),
       ((SELECT id FROM gebeurtenis WHERE naam = 'Aanschaf Nippon Green'),
        (SELECT id FROM interventie WHERE naam = 'CO2-Uitstoot'), 6000),
       #Aanschaf WV Cricket benzine
       ((SELECT id FROM gebeurtenis WHERE naam = 'Aanschaf WV Cricket benzine'),
        (SELECT id FROM interventie WHERE naam = 'CAPEX'), 20000),
       ((SELECT id FROM gebeurtenis WHERE naam = 'Aanschaf WV Cricket benzine'),
        (SELECT id FROM interventie WHERE naam = 'CO2-Uitstoot'), 5000),
       #Aanschaf WV Cricket diesel
       ((SELECT id FROM gebeurtenis WHERE naam = 'Aanschaf WV Cricket diesel'),
        (SELECT id FROM interventie WHERE naam = 'CAPEX'), 22000),
       ((SELECT id FROM gebeurtenis WHERE naam = 'Aanschaf WV Cricket diesel'),
        (SELECT id FROM interventie WHERE naam = 'CO2-Uitstoot'), 5500),
       #Verbruik Elektriciteit
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verbruik elektriciteit'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 0.25),
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verbruik elektriciteit'),
        (SELECT id FROM interventie WHERE naam = 'CO2-Uitstoot'), 0.5),
       #Verbruik benzine
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verbruik benzine'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 1.7),
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verbruik benzine'),
        (SELECT id FROM interventie WHERE naam = 'CO2-Uitstoot'), 2.31),
       #Verbruik diesel
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verbruik diesel'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 1.4),
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verbruik diesel'),
        (SELECT id FROM interventie WHERE naam = 'CO2-Uitstoot'), 2.68),
       #Wegenbelasting WV Cricket benzine
       ((SELECT id FROM gebeurtenis WHERE naam = 'Wegenbelasting WV Cricket benzine'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 488),
       #Wegenbelasting WV Cricket diesel
       ((SELECT id FROM gebeurtenis WHERE naam = 'Wegenbelasting WV Cricket diesel'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 1352),
       #Verzekering Edison 70D (WA)
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verzekering Edison 70D (WA)'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 50),
       #Verzekering Edison 70D (Allrisk)
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verzekering Edison 70D (Allrisk)'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 200),
       #Verzekering Nippon Green (WA)
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verzekering Nippon Green (WA)'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 30),
       #Verzekering Nippon Green (Allrisk)
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verzekering Nippon Green (Allrisk)'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 100),
       #Verzekering WV Cricket benzine (WA)
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verzekering WV Cricket benzine (WA)'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 30),
       #Verzekering WV Cricket benzine (Allrisk)
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verzekering WV Cricket benzine (Allrisk)'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 75),
       #Verzekering WV Cricket diesel (WA)
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verzekering WV Cricket diesel (WA)'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 40),
       #Verzekering WV Cricket diesel (Allrisk)
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verzekering WV Cricket diesel (Allrisk)'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 90),
       #Nieuwe banden (hatchback)
       ((SELECT id FROM gebeurtenis WHERE naam = 'Nieuwe banden (hatchback)'),
        (SELECT id FROM interventie WHERE naam = 'CAPEX'), 50),
       #Nieuwe banden (sedan)
       ((SELECT id FROM gebeurtenis WHERE naam = 'Nieuwe banden (sedan)'),
        (SELECT id FROM interventie WHERE naam = 'CAPEX'), 100),
       #Bandenwissel
       ((SELECT id FROM gebeurtenis WHERE naam = 'Bandenwissel'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 75),
       #APK keuring
       ((SELECT id FROM gebeurtenis WHERE naam = 'APK keuring'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 60),
       #Kleine beurt hatchback
       ((SELECT id FROM gebeurtenis WHERE naam = 'Kleine beurt hatchback'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 120),
       #Kleine beurt sedan
       ((SELECT id FROM gebeurtenis WHERE naam = 'Kleine beurt sedan'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 150),
       #Grote beurt hatchback
       ((SELECT id FROM gebeurtenis WHERE naam = 'Grote beurt hatchback'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 375),
       #Grote beurt sedan
       ((SELECT id FROM gebeurtenis WHERE naam = 'Grote beurt sedan'),
        (SELECT id FROM interventie WHERE naam = 'OPEX'), 500),
       #Verkoop van Edison 70D
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verkoop van Edison 70D'),
        (SELECT id FROM interventie WHERE naam = 'CAPEX'), -9000),
       #Verkoop van Nippon Green
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verkoop van Nippon Green'),
        (SELECT id FROM interventie WHERE naam = 'CAPEX'), -4500),
       #Verkoop van WV Cricket benzine
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verkoop van WV Cricket benzine'),
        (SELECT id FROM interventie WHERE naam = 'CAPEX'), -2500),
       #Verkoop van WV Cricket diesel
       ((SELECT id FROM gebeurtenis WHERE naam = 'Verkoop van WV Cricket diesel'),
        (SELECT id FROM interventie WHERE naam = 'CAPEX'), -2300);

#Aanschaf
INSERT INTO scenario_gebeurtenis (scenario_id, gebeurtenis_id, koppeling_id) VALUE ((SELECT id FROM scenario WHERE naam = 'Edison 70D'),
                                                                                    (SELECT id FROM gebeurtenis WHERE naam = 'Aanschaf Edison 70D'),
                                                                                    1);
INSERT INTO jaren (koppeling_id, jaar, waarde) VALUE (1, 0, 1);

#APK Keuring
INSERT INTO scenario_gebeurtenis (scenario_id, gebeurtenis_id, koppeling_id)
VALUES ((SELECT id FROM scenario WHERE naam = 'Edison 70D'), (SELECT id FROM gebeurtenis WHERE naam = 'APK Keuring'),
        2);

INSERT INTO jaren (koppeling_id, jaar, waarde)
VALUES (2, 4, 1),
       (2, 6, 1),
       (2, 8, 1),
       (2, 9, 1),
       (2, 10, 1),
       (2, 11, 1),
       (2, 12, 1),
       (2, 13, 1),
       (2, 14, 1),
       (2, 15, 1),
       (2, 16, 1),
       (2, 17, 1),
       (2, 18, 1),
       (2, 19, 1),
       (2, 20, 1),
       (2, 21, 1),
       (2, 22, 1);

#Verzekering Edison 70D Allrisk
INSERT INTO scenario_gebeurtenis (scenario_id, gebeurtenis_id, koppeling_id)
VALUES ((SELECT id FROM scenario WHERE naam = 'Edison 70D'),
        (SELECT id FROM gebeurtenis WHERE naam = 'Verzekering Edison 70D (Allrisk)'),
        3);

INSERT INTO jaren (koppeling_id, jaar, waarde)
VALUES (3, 0, 12),
       (3, 1, 12),
       (3, 2, 12),
       (3, 3, 12),
       (3, 4, 12),
       (3, 5, 12),
       (3, 6, 12),
       (3, 7, 12),
       (3, 8, 12),
       (3, 9, 12),
       (3, 10, 12),
       (3, 11, 12),
       (3, 12, 12),
       (3, 13, 12),
       (3, 14, 12),
       (3, 15, 12),
       (3, 16, 12),
       (3, 17, 12),
       (3, 18, 12),
       (3, 19, 12),
       (3, 20, 12);

#Verbruik Elektriciteit
INSERT INTO scenario_gebeurtenis (scenario_id, gebeurtenis_id, koppeling_id)
VALUES ((SELECT id FROM scenario WHERE naam = 'Edison 70D'),
        (SELECT id FROM gebeurtenis WHERE naam = 'Verbruik elektriciteit'),
        4);

INSERT INTO jaren (koppeling_id, jaar, waarde)
VALUES (4, 0, 3000),
       (4, 1, 3000),
       (4, 2, 3000),
       (4, 3, 3000),
       (4, 4, 3000),
       (4, 5, 3000),
       (4, 6, 3000),
       (4, 7, 3000),
       (4, 8, 3000),
       (4, 9, 3000),
       (4, 10, 3000),
       (4, 11, 3000),
       (4, 12, 3000),
       (4, 13, 3000),
       (4, 14, 3000),
       (4, 15, 3000),
       (4, 16, 3000),
       (4, 17, 3000),
       (4, 18, 3000),
       (4, 19, 3000),
       (4, 20, 3000);

#Bandenwissel
INSERT INTO scenario_gebeurtenis (scenario_id, gebeurtenis_id, koppeling_id)
VALUES ((SELECT id FROM scenario WHERE naam = 'Edison 70D'),
        (SELECT id FROM gebeurtenis WHERE naam = 'Bandenwissel'),
        5);

INSERT INTO jaren (koppeling_id, jaar, waarde)
VALUES (5, 0, 1),
       (5, 1, 2),
       (5, 2, 2),
       (5, 3, 2),
       (5, 4, 2),
       (5, 5, 2),
       (5, 6, 2),
       (5, 7, 2),
       (5, 8, 2),
       (5, 9, 2),
       (5, 10, 2),
       (5, 11, 2),
       (5, 12, 2),
       (5, 13, 2),
       (5, 14, 2),
       (5, 15, 2),
       (5, 16, 2),
       (5, 17, 2),
       (5, 18, 2),
       (5, 19, 2),
       (5, 20, 2);

#Nieuwe banden (sedan)
INSERT INTO scenario_gebeurtenis (scenario_id, gebeurtenis_id, koppeling_id)
VALUES ((SELECT id FROM scenario WHERE naam = 'Edison 70D'),
        (SELECT id FROM gebeurtenis WHERE naam = 'Nieuwe banden (sedan)'),
        6);

INSERT INTO jaren (koppeling_id, jaar, waarde)
VALUES (6, 8, 8),
       (6, 16, 8);

#Kleine beurt sedan
INSERT INTO scenario_gebeurtenis (scenario_id, gebeurtenis_id, koppeling_id)
VALUES ((SELECT id FROM scenario WHERE naam = 'Edison 70D'),
        (SELECT id FROM gebeurtenis WHERE naam = 'Kleine beurt sedan'),
        7);

INSERT INTO jaren (koppeling_id, jaar, waarde)
VALUES (7, 1, 1),
       (7, 2, 1),
       (7, 3, 1),
       (7, 5, 1),
       (7, 6, 1),
       (7, 7, 1),
       (7, 9, 1),
       (7, 10, 1),
       (7, 11, 1),
       (7, 13, 1),
       (7, 14, 1),
       (7, 15, 1),
       (7, 17, 1),
       (7, 18, 1),
       (7, 19, 1);

#Grote Beurt Sedan
INSERT INTO scenario_gebeurtenis (scenario_id, gebeurtenis_id, koppeling_id)
VALUES ((SELECT id FROM scenario WHERE naam = 'Edison 70D'),
        (SELECT id FROM gebeurtenis WHERE naam = 'Grote beurt sedan'),
        8);

INSERT INTO jaren (koppeling_id, jaar, waarde)
VALUES (8, 4, 1),
       (8, 9, 1),
       (8, 13, 1),
       (8, 16, 1),
       (8, 18, 1),
       (8, 19, 1);

#Verkoop
INSERT INTO scenario_gebeurtenis (scenario_id, gebeurtenis_id, koppeling_id) VALUE
    ((SELECT id FROM scenario WHERE naam = 'Edison 70D'),
     (SELECT id FROM gebeurtenis WHERE naam = 'Verkoop van Edison 70D'),
     9);

INSERT INTO jaren (koppeling_id, jaar, waarde) VALUE (9, 20, 1);
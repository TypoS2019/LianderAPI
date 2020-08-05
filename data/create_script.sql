DROP DATABASE LCA_API;
CREATE DATABASE LCA_API;

USE LCA_API;

CREATE TABLE scenario
(
  id          INT AUTO_INCREMENT PRIMARY KEY,
  naam        VARCHAR(255) NOT NULL,
  toelichting VARCHAR(255) NULL
);

CREATE TABLE gebeurtenis
(
  id          INT AUTO_INCREMENT PRIMARY KEY,
  naam        VARCHAR(255) NOT NULL,
  toelichting VARCHAR(255) NULL,
  bron        VARCHAR(255) NULL,
  eenheid     VARCHAR(255) NOT NULL
);

CREATE TABLE scenario_gebeurtenis
(
  scenario_id    INT NOT NULL,
  gebeurtenis_id INT NOT NULL,
  koppeling_id   INT AUTO_INCREMENT PRIMARY KEY,
  UNIQUE (scenario_id, gebeurtenis_id),
  FOREIGN KEY (scenario_id) REFERENCES scenario (id) ON DELETE CASCADE,
  FOREIGN KEY (gebeurtenis_id) REFERENCES gebeurtenis (id) ON DELETE CASCADE
);

CREATE TABLE jaren
(
  koppeling_id INT NOT NULL,
  jaar         INT NOT NULL,
  waarde       INT NULL,
  PRIMARY KEY (koppeling_id, jaar),
  FOREIGN KEY (koppeling_id) REFERENCES scenario_gebeurtenis (koppeling_id) ON DELETE CASCADE
);

CREATE TABLE interventie
(
  id          INT AUTO_INCREMENT PRIMARY KEY,
  naam        VARCHAR(255) NOT NULL,
  type        CHAR         NOT NULL,
  eenheid     VARCHAR(255) NOT NULL,
  waarde      FLOAT        NOT NULL,
  toelichting VARCHAR(255) NULL
);

CREATE TABLE gebeurtenis_interventie
(
  gebeurtenis_id INT   NOT NULL,
  interventie_id INT   NOT NULL,
  waarde         FLOAT NULL,
  PRIMARY KEY (gebeurtenis_id, interventie_id),
  FOREIGN KEY (gebeurtenis_id) REFERENCES gebeurtenis (id) ON DELETE CASCADE,
  FOREIGN KEY (interventie_id) REFERENCES interventie (id) ON DELETE CASCADE
);

CREATE TABLE gebruiker_rollen
(
  id  INT AUTO_INCREMENT PRIMARY KEY,
  rol VARCHAR(50) NOT NULL
);

CREATE TABLE gebruiker
(
  id                   INT AUTO_INCREMENT PRIMARY KEY,
  gebruikersnaam       VARCHAR(255) NOT NULL UNIQUE,
  wachtwoord           VARCHAR(255) NOT NULL,
  rol                  INT          NOT NULL,
  tijdelijk_wachtwoord BIT          NOT NULL,
  FOREIGN KEY (rol) REFERENCES gebruiker_rollen (id) ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE project
(
  id    INT AUTO_INCREMENT PRIMARY KEY,
  naam  VARCHAR(255) NOT NULL,
  datum DATE         NOT NULL
);

CREATE TABLE project_gebruiker
(
  gebruiker_id INT NOT NULL,
  project_id   INT NOT NULL,
  PRIMARY KEY (gebruiker_id, project_id),
  FOREIGN KEY (gebruiker_id) REFERENCES gebruiker (id) ON DELETE CASCADE,
  FOREIGN KEY (project_id) REFERENCES project (id) ON DELETE CASCADE
);

CREATE TABLE project_scenario
(
  project_id  INT NOT NULL,
  scenario_id INT NOT NULL,
  PRIMARY KEY (project_id, scenario_id),
  FOREIGN KEY (project_id) REFERENCES project (id) ON DELETE CASCADE,
  FOREIGN KEY (scenario_id) REFERENCES scenario (id) ON DELETE CASCADE
);

CREATE TABLE project_gebeurtenis
(
  project_id     INT NOT NULL,
  gebeurtenis_id INT NOT NULL,
  PRIMARY KEY (project_id, gebeurtenis_id),
  FOREIGN KEY (project_id) REFERENCES project (id) ON DELETE CASCADE,
  FOREIGN KEY (gebeurtenis_id) REFERENCES gebeurtenis (id) ON DELETE CASCADE
);

CREATE TABLE project_interventie
(
  project_id     INT NOT NULL,
  interventie_id INT NOT NULL,
  PRIMARY KEY (project_id, interventie_id),
  FOREIGN KEY (project_id) REFERENCES project (id) ON DELETE CASCADE,
  FOREIGN KEY (interventie_id) REFERENCES interventie (id) ON DELETE CASCADE
);

DELIMITER $$
CREATE PROCEDURE `maak_gebeurtenis_en_stop_in_project`(naam2 varchar(255), toelichting2 varchar(255),
                                                       bron2 varchar(255), eenheid2 varchar(255), project_id2 INT)
BEGIN
  INSERT INTO gebeurtenis(naam, toelichting, bron, eenheid)
  VALUES (naam2, toelichting2, bron2, eenheid2);
  INSERT INTO project_gebeurtenis(project_id, gebeurtenis_id) VALUES (project_id2, LAST_INSERT_ID());

END$$

DELIMITER $$
CREATE PROCEDURE `maak_interventie_en_stop_in_project`(naam2 VARCHAR(255), type2 VARCHAR(255),
                                                       eenheid2 VARCHAR(255), waarde2 FLOAT, toelichting2 VARCHAR(255),
                                                       project_id2 INT)
BEGIN
  INSERT INTO interventie(naam, type, eenheid, waarde, toelichting)
  VALUES (naam2, type2, eenheid2, waarde2, toelichting2);
  INSERT INTO project_interventie(project_id, interventie_id) VALUES (project_id2, LAST_INSERT_ID());

END$$

DELIMITER $$
CREATE PROCEDURE `maak_scenario_en_stop_in_project`(naam2 VARCHAR(255), toelichting2 VARCHAR(255), project_id2 INT)
BEGIN
  INSERT INTO scenario(naam, toelichting)
  VALUES (naam2, toelichting2);
  INSERT INTO project_scenario(project_id, scenario_id) VALUES (project_id2, LAST_INSERT_ID());

END$$

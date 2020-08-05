DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS create_interventie$$
CREATE PROCEDURE create_interventie (naam varchar(255), type char, eenheid varchar(255), waarde float, toelichting varchar(255))
BEGIN
	INSERT INTO interventie (naam, type, eenheid, waarde, toelichting) VALUES (naam, type, eenheid, waarde, toelichting);
END$$


DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS remove_interventie$$
CREATE PROCEDURE remove_interventie (interventie_id int)
BEGIN
	DELETE FROM interventie WHERE id = interventie_id;
END$$

DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS update_interventie$$
CREATE PROCEDURE update_interventie (interventie_id int, naam varchar(255), type char, eenheid varchar(255), waarde float, toelichting varchar(255))
BEGIN
	UPDATE interventie SET naam = naam, type = type, eenheid = eenheid, waarde = waarde, toelichting = toelichting WHERE id = interventie_id;
END$$

DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS select_interventie$$
CREATE PROCEDURE select_interventie (interventie_id int)
BEGIN
	SELECT * FROM interventie WHERE id = interventie_id;
END$$

DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS select_all_interventies$$
CREATE PROCEDURE select_all_interventies ()
BEGIN
	SELECT * FROM interventie;
END$$

DELIMITER $$
CREATE PROCEDURE `maak_interventie_en_stop_in_project`(naam2 varchar(255), type2 varchar(255),
eenheid2 varchar(255), waarde2 float,  toelichting2 varchar(255), project_id2 int)
BEGIN
    INSERT INTO interventie(naam, type, eenheid, waarde, toelichting)
    VALUES (naam2, type2, eenheid2, waarde2, toelichting2);
    INSERT INTO project_interventie(project_id, interventie_id) VALUES (project_id2, LAST_INSERT_ID());

    END$$
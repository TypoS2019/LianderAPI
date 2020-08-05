DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS add_interventie_to_gebeurtenis$$
CREATE PROCEDURE add_interventie_to_gebeurtenis (gebeurtenis_id int, interventie_id int, waarde float)
BEGIN
	INSERT INTO gebeurtenis_interventie (gebeurtenis_id, interventie_id, waarde) VALUES (gebeurtenis_id, interventie_id, waarde);
END$$

DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS remove_interventie_from_gebeurtenis$$
CREATE PROCEDURE remove_interventie_from_gebeurtenis (gebeurtenis_id int, interventie_id int)
BEGIN
	DELETE FROM gebeurtenis_interventie WHERE gebeurtenis_id = gebeurtenis_id & interventie_id = interventie_id;
END$$

DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS update_interventie_from_gebeurtenis$$
CREATE PROCEDURE update_interventie_from_gebeurtenis (gebeurtenis_id int, interventie_id int, waarde float)
BEGIN
	UPDATE gebeurtenis_interventie SET waarde = waarde WHERE gebeurtenis_id = gebeurtenis_id AND interventie_id = interventie_id;
END$$

DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS select_interventie_from_gebeurtenis$$
CREATE PROCEDURE select_interventie_from_gebeurtenis (gebeurtenis_id int, interventie_id int)
BEGIN
	SELECT * FROM gebeurtenis_interventie WHERE gebeurtenis_id = gebeurtenis_id AND interventie_id = interventie_id;
END$$

DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS select_all_interventies_from_gebeurtenis$$
CREATE PROCEDURE select_all_interventies_from_gebeurtenis ()
BEGIN
	SELECT * FROM gebeurtenis_interventie;
END$$
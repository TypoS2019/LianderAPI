DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS create_gebeurtenis$$
CREATE PROCEDURE create_gebeurtenis (naam varchar(255), toelichting varchar(255), bron varchar(255), eenheid varchar(255))
BEGIN
	INSERT INTO gebeurtenis (naam, toelichting, bron, eenheid) VALUES (naam, toelichting, bron, eenheid);
END$$


DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS remove_gebeurtenis$$
CREATE PROCEDURE remove_gebeurtenis (gebeurtenis_id int)
BEGIN
	DELETE FROM gebeurtenis WHERE id = gebeurtenis_id;
END$$

DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS update_gebeurtenis$$
CREATE PROCEDURE update_gebeurtenis (gebeurtenis_id int, naam varchar(255), toelichting varchar(255), bron varchar(255), eenheid varchar(255))
BEGIN
	UPDATE gebeurtenis SET naam = naam, toelichting = toelichting, bron = bron, eenheid = eenheid WHERE id = gebeurtenis_id;
END$$

DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS select_gebeurtenis$$
CREATE PROCEDURE select_gebeurtenis (gebeurtenis_id int)
BEGIN
	SELECT * FROM gebeurtenis WHERE id = gebeurtenis_id;
END$$

DELIMITER $$
USE lca_api$$
DROP PROCEDURE IF EXISTS select_all_gebeurtenissen$$
CREATE PROCEDURE select_all_gebeurtenissen ()
BEGIN
	SELECT * FROM gebeurtenis;
END$$





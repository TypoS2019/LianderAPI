DELIMITER $$
USE `lca_api`$$
DROP procedure IF EXISTS `add_jaar_to_gebeurtenis_for_scenario`;
CREATE PROCEDURE `add_jaar_to_gebeurtenis_for_scenario` (scenario_id int, gebeurtenis_id int, jaar int, waarde int)
BEGIN
	DECLARE id int;
	SELECT koppeling_id into id FROM scenario_gebeurtenis WHERE scenario_id = scenario_id AND gebeurtenis_id = gebeurtenis_id;
	INSERT INTO jaren (koppeling_id, jaar, waarde) VALUES (id, jaar, waarde);
END$$

DELIMITER $$
USE `lca_api`$$
DROP procedure IF EXISTS `remove_jaar_from_gebeurtenis_for_scenario`;
CREATE PROCEDURE `remove_jaar_from_gebeurtenis_for_scenario` (scenario_id int, gebeurtenis_id int)
BEGIN
	DECLARE id int;
	SELECT koppeling_id into id FROM scenario_gebeurtenis WHERE scenario_id = scenario_id AND gebeurtenis_id = gebeurtenis_id;
	DELETE FROM jaren WHERE koppeling_id = id;
END$$

DELIMITER $$
USE `lca_api`$$
DROP procedure IF EXISTS `update_jaar_from_gebeurtenis_for_scenario`;
CREATE PROCEDURE `update_jaar_from_gebeurtenis_for_scenario` (scenario_id int, gebeurtenis_id int, jaar int, waarde int)
BEGIN
	DECLARE id int;
	SELECT koppeling_id into id FROM scenario_gebeurtenis WHERE scenario_id = scenario_id AND gebeurtenis_id = gebeurtenis_id;
	UPDATE jaren SET jaar = jaar, waarde = waarde WHERE koppeling_id = id;
END$$

DELIMITER $$
USE `lca_api`$$
DROP procedure IF EXISTS `select_jaar_from_gebeurtenis_for_scenario`;
CREATE PROCEDURE `select_jaar_from_gebeurtenis_for_scenario` (scenario_id int, gebeurtenis_id int, jaar int, waarde int)
BEGIN
	DECLARE id int;
	SELECT koppeling_id into id FROM scenario_gebeurtenis WHERE scenario_id = scenario_id AND gebeurtenis_id = gebeurtenis_id;
	SELECT * FROM jaren WHERE koppeling_id = id;
END$$

DELIMITER ;
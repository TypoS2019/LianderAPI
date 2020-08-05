DELIMITER $$
USE `lca_api`$$
DROP procedure IF EXISTS `add_gebeurtenis_to_scenario`;
CREATE PROCEDURE `add_gebeurtenis_to_scenario` (scenario_id int, gebeurtenis_id int)
BEGIN
	INSERT INTO scenario_gebeurtenis (scenario_id, gebeurtenis_id) VALUES (scenario_id, gebeurtenis_id);
END$$

DELIMITER $$
USE `lca_api`$$
DROP procedure IF EXISTS `remove_gebeurtenis_from_scenario`;
CREATE PROCEDURE `remove_gebeurtenis_from_scenario` (scenario_id int, gebeurtenis_id int)
BEGIN
	DELETE FROM scenario_gebeurtenis WHERE scenario_id = scenario_id AND gebeurtenis_id;
END$$

DELIMITER $$
USE `lca_api`$$
DROP procedure IF EXISTS `select_gebeurtenis_from_scenario`;
CREATE PROCEDURE `select_gebeurtenis_from_scenario` (scenario_id int, gebeurtenis_id int)
BEGIN
	SELECT * FROM scenario_gebeurtenis WHERE scenario_id = scenario_id AND gebeurtenis_id;
END$$

DELIMITER ;
DELIMITER $$
USE `lca_api`$$
DROP procedure IF EXISTS `add_scenario`;
CREATE PROCEDURE `add_scenario` (naam varchar(255), toelichting varchar(255))
BEGIN
	INSERT INTO scenario (naam, toelichting) VALUES (naam, toelichting);
END$$

DELIMITER $$
USE `lca_api`$$
DROP procedure IF EXISTS `remove_scenario`;
CREATE PROCEDURE `remove_scenario` (scenario_id int)
BEGIN
	DELETE FROM scenario WHERE id = scenario_id;
END$$

DELIMITER $$
USE `lca_api`$$
DROP procedure IF EXISTS `update_scenario`;
CREATE PROCEDURE `update_scenario` (id int, naam varchar(255), toelichting varchar(255))
BEGIN
	UPDATE scenario SET naam = naam, toelichting = toelichting WHERE id = id;
END$$

DELIMITER $$
USE `lca_api`$$
DROP procedure IF EXISTS `select_scenario`;
CREATE PROCEDURE `select_scenario` (scenario_id int)
BEGIN
	SELECT id, naam, toelichting FROM scenario WHERE id = scenario_id;
END$$

DELIMITER $$
USE `lca_api`$$
DROP procedure IF EXISTS `select_all_scenarios`;
CREATE PROCEDURE `select_all_scenarios` ()
BEGIN
	SELECT id, naam, toelichting FROM scenario;
END$$


DELIMITER ;
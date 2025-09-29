CREATE DATABASE `compañero_viaje`;

USE `compañero_viaje`;

DROP TABLE IF EXISTS `compañero_viaje`.`users` ;

CREATE TABLE IF NOT EXISTS `compañero_viaje`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `creado_en` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `compañero_viaje`.`viajes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `compañero_viaje`.`viajes` ;

CREATE TABLE IF NOT EXISTS `compañero_viaje`.`viajes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `viaje` TEXT NOT NULL,
  `autor_id` INT NOT NULL,
  `creado_en` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_viajes_users_idx` (`autor_id` ASC) VISIBLE,
  CONSTRAINT `fk_viajes_users`
    FOREIGN KEY (`autor_id`)
    REFERENCES `compañero_viaje`.`users` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- estos codigos son una extencion que añadi despues cuando me di cuenta que los necesitaba.

USE compañero_viaje;

ALTER TABLE viajes
ADD COLUMN descripcion VARCHAR(255) NOT NULL;

ALTER TABLE viajes
ADD COLUMN fecha_inicio DATE NOT NULL;

ALTER TABLE viajes
ADD COLUMN fecha_fin DATE NOT NULL;



USE compañero_viaje;

ALTER TABLE viajes
CHANGE COLUMN viaje destino VARCHAR(255) NOT NULL;
 
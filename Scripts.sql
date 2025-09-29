-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema compañero_viaje
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `compañero_viaje` ;

-- -----------------------------------------------------
-- Schema compañero_viaje
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `compañero_viaje` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `compañero_viaje` ;

-- -----------------------------------------------------
-- Table `compañero_viaje`.`users`
-- -----------------------------------------------------
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
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `compañero_viaje`.`viajes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `compañero_viaje`.`viajes` ;

CREATE TABLE IF NOT EXISTS `compañero_viaje`.`viajes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `destino` VARCHAR(255) NOT NULL,
  `autor_id` INT NOT NULL,
  `creado_en` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `descripcion` VARCHAR(255) NOT NULL,
  `fecha_inicio` DATE NOT NULL,
  `fecha_fin` DATE NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_viajes_users_idx` (`autor_id` ASC) VISIBLE,
  CONSTRAINT `fk_viajes_users`
    FOREIGN KEY (`autor_id`)
    REFERENCES `compañero_viaje`.`users` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

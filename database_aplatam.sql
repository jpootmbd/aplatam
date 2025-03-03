CREATE DATABASE APLATAM;
CREATE TABLE APLATAM.noticias (
	id_author INT(11) NULL DEFAULT NULL,
	id_source_name INT(11) NULL DEFAULT NULL,
	published_date DATE NULL DEFAULT NULL
)
COMMENT='se guardan las noticiar recien descargadas del servicio web'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;
CREATE TABLE APLATAM.abt_noticias_resumen (
	id_author INT(11) NULL DEFAULT NULL,
	id_source_name INT(11) NULL DEFAULT NULL,
	total_news INT(11) NULL DEFAULT NULL,
	min_published_date DATE NULL DEFAULT NULL,
	max_published_date DATE NULL DEFAULT NULL,
	published_date DATE NULL DEFAULT NULL
)
COMMENT='se guardan las noticiar recien descargadas del servicio web'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;

CREATE TABLE APLATAM.noticias_temp (
	author VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	source_name VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	published_date DATE NULL DEFAULT NULL
)
COMMENT='se guardan las noticiar recien descargadas del servicio web'
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;

CREATE TABLE APLATAM.cat_author (
	id INT(11) NOT NULL AUTO_INCREMENT,
	author VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	PRIMARY KEY (id) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;


CREATE TABLE APLATAM.cat_source (
	id INT(11) NOT NULL AUTO_INCREMENT,
	source_name VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;
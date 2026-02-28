-- Schema for PropTech propiedades database
-- Table: propiedades
-- Real estate properties (casa, departamento, terreno, etc.)
CREATE TABLE IF NOT EXISTS propiedades (
    id                 INT             NOT NULL AUTO_INCREMENT,
    titulo             VARCHAR(255)    NOT NULL,
    descripcion        TEXT            NULL,
    tipo               VARCHAR(64)     NOT NULL COMMENT 'casa, departamento, terreno, etc.',
    precio             DECIMAL(14, 2)  NOT NULL,
    habitaciones       INT             NULL,
    banos              INT             NULL,
    area_m2            DECIMAL(10, 2)  NULL,
    ubicacion          VARCHAR(255)    NULL,
    fecha_publicacion  DATE            NULL,
    PRIMARY KEY (id),
    INDEX idx_tipo (tipo),
    INDEX idx_precio (precio),
    INDEX idx_ubicacion (ubicacion(100)),
    INDEX idx_fecha_publicacion (fecha_publicacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

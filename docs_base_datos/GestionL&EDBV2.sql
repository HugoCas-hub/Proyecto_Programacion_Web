CREATE DATABASE gestion_documentos;
USE gestion_documentos;

-- =========================
-- TABLA USUARIOS
-- =========================
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    rol ENUM('admin', 'empleado') DEFAULT 'empleado',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- TABLA CLIENTES
-- =========================
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion VARCHAR(150)
);

-- =========================
-- TABLA TIPOS DE DOCUMENTOS
-- =========================
CREATE TABLE tipos_documentos (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(100) NOT NULL,
    dias_alerta INT DEFAULT 30
);

INSERT INTO tipos_documentos (nombre_tipo) VALUES
('Predial'),
('Licencia de Operación'),
('Licencia de Anuncios'),
('Contrato de Basura'),
('Línea Exclusiva'),
('Certificado Medidas de Seguridad'),
('Exención de Aguas'),
('Atrapa la Grasa'),
('Atrapa la Pelusa');

-- =========================
-- TABLA ESTADOS (REEMPLAZA ENUM)
-- =========================
CREATE TABLE estados_documento (
    id_estado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    color VARCHAR(20)
);

INSERT INTO estados_documento (nombre, color) VALUES
('vigente','verde'),
('proximo','amarillo'),
('vencido','rojo'),
('en_tramite','azul'),
('pendiente','naranja'),
('detenido','rojo'),
('n/a','gris'),
('particular','morado');

-- =========================
-- TABLA DOCUMENTOS (MEJORADA)
-- =========================
CREATE TABLE documentos (
    id_documento INT AUTO_INCREMENT PRIMARY KEY,

    id_cliente INT NOT NULL,
    id_tipo INT NOT NULL,
    id_estado INT,

    fecha_vencimiento DATE,

    notas TEXT,
    fecha_detencion DATE,

    -- ARCHIVO EN BASE DE DATOS
    archivo LONGBLOB,
    nombre_archivo VARCHAR(255),
    tipo_mime VARCHAR(100),
    tamano INT,

    creado_por INT,
    modificado_por INT,

    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo) REFERENCES tipos_documentos(id_tipo) ON DELETE CASCADE,
    FOREIGN KEY (id_estado) REFERENCES estados_documento(id_estado),

    FOREIGN KEY (creado_por) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (modificado_por) REFERENCES usuarios(id_usuario)
);

-- =========================
-- TABLA NOTIFICACIONES
-- =========================
CREATE TABLE notificaciones (
    id_notificacion INT AUTO_INCREMENT PRIMARY KEY,

    id_documento INT,
    id_usuario INT,

    mensaje TEXT,
    tipo ENUM('alerta','vencido'),

    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    enviado BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (id_documento) REFERENCES documentos(id_documento) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- =========================
-- TABLA HISTORIAL (AUDITORÍA)
-- =========================
CREATE TABLE historial_documentos (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_documento INT,
    estado_anterior VARCHAR(50),
    estado_nuevo VARCHAR(50),
    fecha_cambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_usuario INT,
    comentario TEXT,

    FOREIGN KEY (id_documento) REFERENCES documentos(id_documento) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- =========================
-- CONFIGURACIÓN DE ALERTAS
-- =========================
CREATE TABLE configuracion_alertas (
    id_config INT AUTO_INCREMENT PRIMARY KEY,
    dias_rojo INT,
    dias_amarillo INT,
    activo BOOLEAN DEFAULT TRUE,
    id_tipo INT,
	FOREIGN KEY (id_tipo) REFERENCES tipos_documentos(id_tipo)
);

INSERT INTO configuracion_alertas (dias_rojo, dias_amarillo)
VALUES (10, 60);

-- =========================
-- TABLA REPORTES
-- =========================
CREATE TABLE reportes (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    tipo_reporte VARCHAR(100),
    fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    generado_por INT,
    parametros JSON,

    FOREIGN KEY (generado_por) REFERENCES usuarios(id_usuario)
);

-- =========================
-- TABLA LOGS (EVENTOS DEL SISTEMA)
-- =========================
CREATE TABLE logs (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    accion VARCHAR(100),
    tabla_afectada VARCHAR(50),
    id_registro INT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_usuario INT,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- =========================
-- CONSULTA MEJORADA SEMÁFORO
-- =========================
SELECT 
    d.id_documento,
    c.nombre AS cliente,
    t.nombre_tipo,
    d.fecha_vencimiento,

    DATEDIFF(d.fecha_vencimiento, CURDATE()) AS dias_restantes,

    CASE
        WHEN d.fecha_vencimiento < CURDATE() THEN 'rojo'
        WHEN DATEDIFF(d.fecha_vencimiento, CURDATE()) <= 
            (SELECT dias_rojo FROM configuracion_alertas WHERE activo = TRUE LIMIT 1)
            THEN 'rojo'
        WHEN DATEDIFF(d.fecha_vencimiento, CURDATE()) <= 
            (SELECT dias_amarillo FROM configuracion_alertas WHERE activo = TRUE LIMIT 1)
            THEN 'amarillo'
        ELSE 'verde'
    END AS semaforo
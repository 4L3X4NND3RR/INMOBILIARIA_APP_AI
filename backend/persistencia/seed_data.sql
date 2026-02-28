-- Seed data: 15-20 sample properties for PropTech search

USE inmobiliaria;

INSERT INTO propiedades (titulo, descripcion, tipo, precio, habitaciones, banos, area_m2, ubicacion, fecha_publicacion) VALUES
('Casa amplia zona 10', 'Hermosa casa con jardín y garaje para 2 autos. Cerca de centros comerciales.', 'casa', 285000.00, 4, 3, 220.00, 'Zona 10', '2025-01-15'),
('Departamento moderno zona 15', 'Apartamento con vista, acabados de lujo. Incluye parqueo.', 'departamento', 145000.00, 2, 2, 95.00, 'Zona 15', '2025-02-01'),
('Terreno comercial zona 12', 'Terreno plano, ideal para construcción o inversión. Servicios disponibles.', 'terreno', 85000.00, NULL, NULL, 350.00, 'Zona 12', '2024-11-20'),
('Casa 3 habitaciones zona 10', 'Casa familiar en condominio cerrado. Seguridad 24 horas.', 'casa', 195000.00, 3, 2, 150.00, 'Zona 10', '2025-02-10'),
('Departamento económico zona 7', 'Departamento funcional, buen precio. Cerca de transporte público.', 'departamento', 75000.00, 2, 1, 65.00, 'Zona 7', '2025-01-28'),
('Casa con piscina zona 14', 'Residencia de lujo con piscina y jardín. 4 habitaciones, estudio.', 'casa', 420000.00, 4, 4, 380.00, 'Zona 14', '2024-12-05'),
('Local comercial zona 5', 'Local en esquina, alto tráfico. Ideal para negocio.', 'local', 120000.00, NULL, 1, 120.00, 'Zona 5', '2025-02-15'),
('Departamento 2 habitaciones zona 15', 'Apartamento cómodo, 2 baños. Área de lavandería.', 'departamento', 135000.00, 2, 2, 88.00, 'Zona 15', '2025-01-20'),
('Terreno residencial zona 9', 'Terreno para construir tu casa. Servicios básicos.', 'terreno', 55000.00, NULL, NULL, 200.00, 'Zona 9', '2024-10-12'),
('Casa 5 habitaciones zona 11', 'Casa grande para familia. Sala, comedor, jardín interior.', 'casa', 310000.00, 5, 3, 280.00, 'Zona 11', '2025-02-08'),
('Departamento menos de 150000 zona 4', 'Bonito departamento, bien ubicado. Un baño completo.', 'departamento', 98000.00, 2, 1, 72.00, 'Zona 4', '2025-01-05'),
('Casa 3 baños zona 16', 'Casa con 3 baños y más de 150 m². Garaje y bodega.', 'casa', 175000.00, 3, 3, 165.00, 'Zona 16', '2025-02-12'),
('Terreno entre 50000 y 100000', 'Terreno en venta, precio negociable. Zona en desarrollo.', 'terreno', 72000.00, NULL, NULL, 180.00, 'Zona 8', '2025-01-30'),
('Departamento reciente zona 10', 'Departamento nuevo, publicado hace 2 semanas. 2 habitaciones.', 'departamento', 158000.00, 2, 2, 92.00, 'Zona 10', '2025-02-14'),
('Casa publicada últimos 30 días', 'Casa familiar, 3 habitaciones. Oportunidad.', 'casa', 210000.00, 3, 2, 140.00, 'Zona 13', '2025-02-20'),
('Oficina zona 10', 'Oficina lista para usar. Aire acondicionado, recepción.', 'oficina', 185000.00, 3, 2, 110.00, 'Zona 10', '2024-12-18'),
('Departamento 2 habitaciones zona 15', 'Segundo departamento en zona 15. Bien iluminado.', 'departamento', 142000.00, 2, 2, 85.00, 'Zona 15', '2025-02-05'),
('Casa 4 habitaciones zona 7', 'Casa amplia con patio. Precio accesible.', 'casa', 165000.00, 4, 2, 190.00, 'Zona 7', '2025-01-12'),
('Terreno zona 6', 'Terreno comercial/residencial. Documentación en orden.', 'terreno', 95000.00, NULL, NULL, 250.00, 'Zona 6', '2024-11-28'),
('Departamento vista zona 14', 'Departamento con más de 2 baños y 150 m². Vista a montaña.', 'departamento', 198000.00, 3, 3, 155.00, 'Zona 14', '2025-02-18');

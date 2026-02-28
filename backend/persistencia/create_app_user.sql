-- Create a read-only user for the PropTech API (search/read only on propiedades).
-- Run this script as a user with GRANT privilege (e.g. root or DBA).
-- Replace 'proptech_ro' and 'YOUR_SECURE_PASSWORD' before running.

-- Database and table used by the app (must exist; see schema.sql)
-- Database: inmobiliaria
-- Table: propiedades

-- Create the user (MySQL 5.7+ / MariaDB 10.2+)
-- Use 'proptech_ro'@'localhost' for local-only; use 'proptech_ro'@'%' for remote (e.g. Docker).
CREATE USER IF NOT EXISTS 'proptech_ro'@'%'
  IDENTIFIED BY 'your_app_password';

-- Grant only SELECT on propiedades (read and search)
GRANT SELECT ON inmobiliaria.propiedades TO 'proptech_ro'@'%';

-- Apply privilege changes
FLUSH PRIVILEGES;

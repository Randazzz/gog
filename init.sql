DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'gog_username_prod') THEN
        CREATE ROLE gog_username_prod WITH LOGIN PASSWORD 'gog_password_prod';
    END IF;
END $$;

CREATE DATABASE gog_db_prod OWNER gog_username_prod;

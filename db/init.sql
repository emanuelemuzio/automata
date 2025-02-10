SELECT 'CREATE DATABASE pgdb'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'pgdb')\gexec

SELECT 'CREATE DATABASE pgvdb'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'pgvdb')\gexec

\connect pgdb;

CREATE TABLE IF NOT EXISTS public."user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    pwd TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    disabled BOOLEAN NOT NULL DEFAULT false,
    role VARCHAR(50) NOT NULL CHECK (role IN ('ADMIN', 'USER'))
);

INSERT INTO public."user" (
    username, 
    full_name, 
    pwd, 
    disabled, 
    "role"
)
SELECT 'admin@admin.com', 
       'Admin Admin', 
       '$2b$12$NigxHJksm0nubBshTQkXJOR3YOCWR1WA4hWSuxMh0AAPkLu2V4ux2', 
       false, 
       'ADMIN'
WHERE NOT EXISTS (
    SELECT 1 FROM public."user" WHERE username = 'admin@admin.com'
);
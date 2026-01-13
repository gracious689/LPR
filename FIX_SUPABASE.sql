-- Fix Supabase PostgREST Configuration
-- Run this SQL in your Supabase SQL Editor

-- 1. Enable schema exposure for PostgREST
-- This allows the API to access the public schema
ALTER ROLE postgres SET "app_settings.current_schema" TO 'public';

-- 2. Add the public schema to exposed schemas
-- This tells PostgREST to expose the public schema
INSERT INTO public.pgrst_settings (name, value)
VALUES ('db-schemas', 'public')
ON CONFLICT (name) DO UPDATE SET value = 'public';

-- 3. Grant necessary permissions
GRANT USAGE ON SCHEMA public TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- 4. Refresh PostgREST schema cache
-- This makes PostgREST aware of the new configuration
NOTIFY pgrst;

-- 5. Verify table exists and has proper permissions
SELECT 
    table_name,
    table_schema,
    has_table_privilege('postgres', table_name, 'SELECT') as can_select,
    has_table_privilege('postgres', table_name, 'INSERT') as can_insert,
    has_table_privilege('postgres', table_name, 'UPDATE') as can_update,
    has_table_privilege('postgres', table_name, 'DELETE') as can_delete
FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name = 'license_plates';

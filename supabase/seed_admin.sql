-- =====================================================================
-- Seed the OZTECH Bathrooms admin account.
--
-- 1. Run the migration in supabase/migrations first.
-- 2. Replace CHANGE-ME-TO-A-STRONG-PASSWORD below (do not commit it).
-- 3. Run this whole script in the Supabase SQL editor.
--
-- Safe to re-run: if the user already exists, the password is reset to
-- the value below and the account is (re)granted admin access.
-- =====================================================================

do $$
declare
  v_email    text := 'info@oztechbathrooms.com.au';
  v_password text := 'CHANGE-ME-TO-A-STRONG-PASSWORD';
  v_user_id  uuid;
begin
  if v_password = 'CHANGE-ME-TO-A-STRONG-PASSWORD' or length(v_password) < 10 then
    raise exception 'Set a real password (10+ characters) in v_password before running this script.';
  end if;

  select id into v_user_id from auth.users where lower(email) = lower(v_email);

  if v_user_id is null then
    v_user_id := gen_random_uuid();

    insert into auth.users (
      instance_id, id, aud, role, email, encrypted_password,
      email_confirmed_at, raw_app_meta_data, raw_user_meta_data,
      created_at, updated_at,
      confirmation_token, email_change, email_change_token_new, recovery_token
    ) values (
      '00000000-0000-0000-0000-000000000000', v_user_id, 'authenticated', 'authenticated',
      v_email, extensions.crypt(v_password, extensions.gen_salt('bf')),
      now(), '{"provider":"email","providers":["email"]}'::jsonb, '{}'::jsonb,
      now(), now(),
      '', '', '', ''
    );

    insert into auth.identities (
      id, user_id, provider_id, identity_data, provider,
      last_sign_in_at, created_at, updated_at
    ) values (
      gen_random_uuid(), v_user_id, v_user_id::text,
      jsonb_build_object('sub', v_user_id::text, 'email', v_email, 'email_verified', true),
      'email', now(), now(), now()
    );
  else
    update auth.users
       set encrypted_password = extensions.crypt(v_password, extensions.gen_salt('bf')),
           email_confirmed_at = coalesce(email_confirmed_at, now()),
           updated_at = now()
     where id = v_user_id;
  end if;

  insert into public.admins (user_id) values (v_user_id)
  on conflict (user_id) do nothing;

  raise notice 'Admin ready: % (%)', v_email, v_user_id;
end
$$;

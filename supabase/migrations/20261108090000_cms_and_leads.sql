-- =====================================================================
-- OZTECH Bathrooms: CMS + leads schema
-- Tables: admins, site_content, page_sections, leads
-- Storage: site-media (public bucket, admin-only writes)
-- =====================================================================

-- ---------------------------------------------------------------------
-- Admins
-- ---------------------------------------------------------------------
create table if not exists public.admins (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  created_at timestamptz not null default now()
);

alter table public.admins enable row level security;

drop policy if exists "Admins can read own row" on public.admins;
create policy "Admins can read own row"
  on public.admins for select
  to authenticated
  using (user_id = (select auth.uid()));

-- Returns true when the current user is an admin. SECURITY DEFINER so it
-- can be used inside RLS policies on other tables without recursion.
create or replace function public.is_admin()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.admins a where a.user_id = (select auth.uid())
  );
$$;

revoke all on function public.is_admin() from public;
grant execute on function public.is_admin() to anon, authenticated;

-- ---------------------------------------------------------------------
-- updated_at helper
-- ---------------------------------------------------------------------
create or replace function public.set_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

-- ---------------------------------------------------------------------
-- Site content: key/value overrides for copy, images, links, SEO and
-- business information.
--   <page>:<hash>.<n>          copy override (HTML)
--   <page>:<hash>.<n>@href     link override
--   <page>:img:<hash>.<n>      image URL override (and @alt)
--   g:...                      shared header/footer content
--   hide:<page>:<index>        hide a built-in section ("1")
--   seo:<page>:title|description
--   biz.<field>                business information
-- ---------------------------------------------------------------------
create table if not exists public.site_content (
  key        text primary key check (char_length(key) between 1 and 200),
  value      text not null default '' check (char_length(value) <= 20000),
  updated_at timestamptz not null default now(),
  updated_by uuid references auth.users (id) on delete set null default auth.uid()
);

drop trigger if exists site_content_updated_at on public.site_content;
create trigger site_content_updated_at
  before update on public.site_content
  for each row execute function public.set_updated_at();

alter table public.site_content enable row level security;

drop policy if exists "Public can read site content" on public.site_content;
create policy "Public can read site content"
  on public.site_content for select
  to anon, authenticated
  using (true);

drop policy if exists "Admins can insert site content" on public.site_content;
create policy "Admins can insert site content"
  on public.site_content for insert
  to authenticated
  with check ((select public.is_admin()));

drop policy if exists "Admins can update site content" on public.site_content;
create policy "Admins can update site content"
  on public.site_content for update
  to authenticated
  using ((select public.is_admin()))
  with check ((select public.is_admin()));

drop policy if exists "Admins can delete site content" on public.site_content;
create policy "Admins can delete site content"
  on public.site_content for delete
  to authenticated
  using ((select public.is_admin()));

-- Default business information
insert into public.site_content (key, value) values
  ('biz.business_name', 'OZTECH Bathrooms'),
  ('biz.phone',         '0466 877 871'),
  ('biz.email',         'info@oztechbathrooms.com.au'),
  ('biz.service_area',  'Greater Sydney, NSW'),
  ('biz.licence',       ''),
  ('biz.abn',           ''),
  ('biz.hours',         ''),
  ('biz.facebook',      ''),
  ('biz.instagram',     ''),
  ('biz.logo',          '')
on conflict (key) do nothing;

-- ---------------------------------------------------------------------
-- Custom page sections added by the admin
-- ---------------------------------------------------------------------
create table if not exists public.page_sections (
  id            uuid primary key default gen_random_uuid(),
  page          text not null check (page ~ '^[a-z0-9-]{1,60}$'),
  after_section integer not null default 0 check (after_section >= 0),
  position      integer not null default 0,
  type          text not null check (type in ('text', 'image_text', 'gallery', 'features', 'cta')),
  data          jsonb not null default '{}'::jsonb,
  published     boolean not null default true,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

create index if not exists page_sections_page_idx
  on public.page_sections (page, after_section, position);

drop trigger if exists page_sections_updated_at on public.page_sections;
create trigger page_sections_updated_at
  before update on public.page_sections
  for each row execute function public.set_updated_at();

alter table public.page_sections enable row level security;

drop policy if exists "Public can read published sections" on public.page_sections;
create policy "Public can read published sections"
  on public.page_sections for select
  to anon, authenticated
  using (published or (select public.is_admin()));

drop policy if exists "Admins can insert sections" on public.page_sections;
create policy "Admins can insert sections"
  on public.page_sections for insert
  to authenticated
  with check ((select public.is_admin()));

drop policy if exists "Admins can update sections" on public.page_sections;
create policy "Admins can update sections"
  on public.page_sections for update
  to authenticated
  using ((select public.is_admin()))
  with check ((select public.is_admin()));

drop policy if exists "Admins can delete sections" on public.page_sections;
create policy "Admins can delete sections"
  on public.page_sections for delete
  to authenticated
  using ((select public.is_admin()));

-- ---------------------------------------------------------------------
-- One round trip for the public site: all content + this page's sections
-- ---------------------------------------------------------------------
create or replace function public.get_page(p_page text)
returns jsonb
language sql
stable
security invoker
set search_path = ''
as $$
  select jsonb_build_object(
    'content', coalesce(
      (select jsonb_object_agg(c.key, c.value)
         from public.site_content c
        where c.key like 'biz.%'
           or c.key like 'g:%'
           or c.key like p_page || ':%'
           or c.key like 'hide:' || p_page || ':%'
           or c.key like 'seo:' || p_page || ':%'),
      '{}'::jsonb),
    'sections', coalesce(
      (select jsonb_agg(
                jsonb_build_object(
                  'id', s.id,
                  'after_section', s.after_section,
                  'type', s.type,
                  'data', s.data)
                order by s.after_section, s.position, s.created_at)
         from public.page_sections s
        where s.page = p_page and s.published),
      '[]'::jsonb)
  );
$$;

grant execute on function public.get_page(text) to anon, authenticated;

-- ---------------------------------------------------------------------
-- Leads (inserted by the submit-lead edge function with the service role)
-- ---------------------------------------------------------------------
create table if not exists public.leads (
  id          uuid primary key default gen_random_uuid(),
  created_at  timestamptz not null default now(),
  source      text not null default 'website',
  page        text,
  service     text,
  timeframe   text,
  name        text not null,
  email       text not null,
  phone       text not null,
  postcode    text,
  suburb      text,
  message     text,
  status      text not null default 'new'
              check (status in ('new', 'contacted', 'quoted', 'won', 'lost')),
  notes       text,
  email_sent  boolean not null default false,
  user_agent  text
);

create index if not exists leads_created_at_idx on public.leads (created_at desc);
create index if not exists leads_email_idx on public.leads (lower(email), created_at desc);

alter table public.leads enable row level security;

drop policy if exists "Admins can read leads" on public.leads;
create policy "Admins can read leads"
  on public.leads for select
  to authenticated
  using ((select public.is_admin()));

drop policy if exists "Admins can update leads" on public.leads;
create policy "Admins can update leads"
  on public.leads for update
  to authenticated
  using ((select public.is_admin()))
  with check ((select public.is_admin()));

drop policy if exists "Admins can delete leads" on public.leads;
create policy "Admins can delete leads"
  on public.leads for delete
  to authenticated
  using ((select public.is_admin()));

-- No insert policy: the public cannot write to leads directly.

-- ---------------------------------------------------------------------
-- Storage: site-media bucket (public read, admin write)
-- ---------------------------------------------------------------------
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'site-media', 'site-media', true, 10485760,
  array['image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/svg+xml', 'image/avif']
)
on conflict (id) do update
  set public = excluded.public,
      file_size_limit = excluded.file_size_limit,
      allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "Admins can list site media" on storage.objects;
create policy "Admins can list site media"
  on storage.objects for select
  to authenticated
  using (bucket_id = 'site-media' and (select public.is_admin()));

drop policy if exists "Admins can upload site media" on storage.objects;
create policy "Admins can upload site media"
  on storage.objects for insert
  to authenticated
  with check (bucket_id = 'site-media' and (select public.is_admin()));

drop policy if exists "Admins can update site media" on storage.objects;
create policy "Admins can update site media"
  on storage.objects for update
  to authenticated
  using (bucket_id = 'site-media' and (select public.is_admin()))
  with check (bucket_id = 'site-media' and (select public.is_admin()));

drop policy if exists "Admins can delete site media" on storage.objects;
create policy "Admins can delete site media"
  on storage.objects for delete
  to authenticated
  using (bucket_id = 'site-media' and (select public.is_admin()));

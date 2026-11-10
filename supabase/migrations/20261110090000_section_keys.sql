-- Attach custom sections to a built-in section by its stable key (e.g. "process-title")
-- instead of only its position, so they stay in the right place when the page layout
-- changes. after_section (position) is kept as a fallback for older rows.
alter table public.page_sections
  add column if not exists after_key text check (after_key is null or char_length(after_key) <= 120);

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
                  'after_key', s.after_key,
                  'type', s.type,
                  'data', s.data)
                order by s.after_section, s.position, s.created_at)
         from public.page_sections s
        where s.page = p_page and s.published),
      '[]'::jsonb)
  );
$$;

grant execute on function public.get_page(text) to anon, authenticated;

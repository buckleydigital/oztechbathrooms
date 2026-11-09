-- Allow "before_after" custom sections (drag-to-compare photo sliders).
alter table public.page_sections drop constraint if exists page_sections_type_check;
alter table public.page_sections
  add constraint page_sections_type_check
  check (type in ('text', 'image_text', 'gallery', 'features', 'cta', 'before_after'));

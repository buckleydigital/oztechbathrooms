# OZTECH Bathrooms: Website

Static website for OZTECH Bathrooms, Sydney, with a Supabase backend for leads and an admin area for editing the site.

## Structure
- `index.html`, service pages, `get-a-quote.html`, `privacy-policy.html`, `terms.html`: public pages (default content lives in the HTML)
- `assets/js/config.js`: Supabase URL and publishable key
- `assets/js/cms.js`: loads admin edits (copy, images, links, hidden sections, SEO, business info, custom sections) and applies them over the defaults. If Supabase is unreachable the site shows the defaults.
- `assets/js/quote.js`: the step-by-step quote survey
- `admin/`: admin sign-in and dashboard (`/admin/`)
- `supabase/migrations/`: database schema, security policies and storage bucket
- `supabase/functions/submit-lead/`: receives leads, stores them and emails them via Resend
- `supabase/seed_admin.sql`: creates the admin login
- `tools/build_site.py`: regenerates the HTML pages (developers only)

## Deploying the backend

1. **Run the migration.** Paste `supabase/migrations/20261108090000_cms_and_leads.sql` into the Supabase SQL editor and run it, or use the CLI:
   ```bash
   supabase link --project-ref vspxonolprsrlupvlojp
   supabase db push
   ```
2. **Deploy the lead function** (JWT verification must be off because the site uses the publishable key):
   ```bash
   supabase functions deploy submit-lead --no-verify-jwt --project-ref vspxonolprsrlupvlojp
   ```
3. **Email sending.** `RESEND_API_KEY` must be set in Edge Function secrets. Leads go to `info@oztechbathrooms.com.au`.
   Until `oztechbathrooms.com.au` is verified in Resend, the function sends from `onboarding@resend.dev`, which Resend only delivers to the email address that owns the Resend account. After verifying the domain, set the sender:
   ```bash
   supabase secrets set LEAD_FROM_EMAIL="OZTECH Bathrooms Website <leads@oztechbathrooms.com.au>" --project-ref vspxonolprsrlupvlojp
   ```
4. **Create the admin login.** Open `supabase/seed_admin.sql`, set a password, and run it in the SQL editor. Don't commit the password.
5. **Password reset links.** In Supabase, go to Authentication, then URL Configuration. Set Site URL to the live site and add `https://<your-domain>/admin/` to Redirect URLs.

## Admin
Go to `/admin/` and sign in. Tabs:
- **Leads**: every enquiry, with status, notes and CSV export
- **Page editor**: click text on any page to edit it, click images to replace them, turn sections on or off
- **Sections**: add new sections (text, image and text, gallery, feature list, call to action) anywhere on a page
- **Business info**: phone, email, service area, licence number, ABN, hours, social links and logo
- **Media**: upload and manage images
- **SEO**: page titles and descriptions

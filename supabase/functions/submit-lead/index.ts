// submit-lead
// Receives quote requests from the website, stores them in public.leads
// and emails each one to the business via Resend.
//
// Secrets / env:
//   RESEND_API_KEY        (required) Resend API key
//   LEAD_NOTIFY_EMAIL     (optional) default info@oztechbathrooms.com.au
//   LEAD_FROM_EMAIL       (optional) default "OZTECH Bathrooms Website <onboarding@resend.dev>"
//                         Use an address on a domain verified in Resend.
//   SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY are provided automatically.
//
// Deploy without JWT verification (the site calls it with the publishable key):
//   supabase functions deploy submit-lead --no-verify-jwt

import { createClient } from "npm:@supabase/supabase-js@2.45.4";

const NOTIFY_EMAIL = Deno.env.get("LEAD_NOTIFY_EMAIL") ?? "info@oztechbathrooms.com.au";
const FROM_EMAIL = Deno.env.get("LEAD_FROM_EMAIL") ?? "OZTECH Bathrooms Website <onboarding@resend.dev>";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}

function clean(v: unknown, max: number): string {
  if (typeof v !== "string") return "";
  return v.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "").trim().slice(0, max);
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
  if (req.method !== "POST") return json({ error: "Method not allowed" }, 405);

  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return json({ error: "Invalid request." }, 400);
  }

  // Honeypot: bots fill hidden fields. Pretend success, store nothing.
  if (clean(body.company, 200)) return json({ ok: true });

  const lead = {
    source: clean(body.source, 40) || "website",
    page: clean(body.page, 120) || null,
    service: clean(body.service, 120) || null,
    timeframe: clean(body.timeframe, 120) || null,
    name: clean(body.name, 120),
    email: clean(body.email, 200).toLowerCase(),
    phone: clean(body.phone, 40),
    postcode: clean(body.postcode, 10) || null,
    suburb: clean(body.suburb, 120) || null,
    message: clean(body.message, 4000) || null,
    user_agent: clean(req.headers.get("user-agent") ?? "", 300) || null,
  };

  const errors: string[] = [];
  if (lead.name.length < 2) errors.push("Please enter your name.");
  if (!EMAIL_RE.test(lead.email)) errors.push("Please enter a valid email address.");
  const digits = lead.phone.replace(/\D/g, "");
  if (digits.length < 8 || digits.length > 15) errors.push("Please enter a valid phone number.");
  if (lead.postcode && !/^\d{4}$/.test(lead.postcode)) errors.push("Please enter a valid 4-digit postcode.");
  if (errors.length) return json({ error: errors.join(" ") }, 422);

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    { auth: { persistSession: false } },
  );

  // Basic flood protection: max 3 submissions per email per 10 minutes.
  const since = new Date(Date.now() - 10 * 60 * 1000).toISOString();
  const { count } = await supabase
    .from("leads")
    .select("id", { count: "exact", head: true })
    .eq("email", lead.email)
    .gte("created_at", since);
  if ((count ?? 0) >= 3) {
    return json({ error: "We've already received your enquiry. We'll be in touch shortly." }, 429);
  }

  const { data: inserted, error: insertError } = await supabase
    .from("leads")
    .insert(lead)
    .select("id, created_at")
    .single();

  if (insertError) {
    console.error("Lead insert failed", insertError);
    return json({ error: "Sorry, something went wrong. Please call us instead." }, 500);
  }

  // Email notification
  let emailSent = false;
  const apiKey = Deno.env.get("RESEND_API_KEY");
  if (apiKey) {
    const rows: [string, string | null][] = [
      ["Name", lead.name],
      ["Phone", lead.phone],
      ["Email", lead.email],
      ["Postcode", lead.postcode],
      ["Suburb", lead.suburb],
      ["Looking for", lead.service],
      ["Timeframe", lead.timeframe],
      ["Message", lead.message],
      ["Form", lead.source],
      ["Page", lead.page],
    ];
    const tableRows = rows
      .filter(([, v]) => v)
      .map(([k, v]) =>
        `<tr><td style="padding:10px 16px 10px 0;color:#6b6b6b;font-size:13px;text-transform:uppercase;letter-spacing:.08em;vertical-align:top;white-space:nowrap">${k}</td>` +
        `<td style="padding:10px 0;font-size:15px;color:#0a0a0a;white-space:pre-wrap">${escapeHtml(v!)}</td></tr>`
      )
      .join("");
    const tel = lead.phone.replace(/[^\d+]/g, "");
    const html = `<!doctype html><html><body style="margin:0;background:#f5f5f3;font-family:Helvetica,Arial,sans-serif">
<div style="max-width:600px;margin:0 auto;padding:32px 16px">
  <div style="background:#0a0a0a;color:#fff;padding:24px 28px">
    <div style="font-size:12px;letter-spacing:.28em;text-transform:uppercase;color:#b9b9b6">New website lead</div>
    <div style="font-size:24px;margin-top:8px;font-family:Georgia,serif">${escapeHtml(lead.name)}</div>
  </div>
  <div style="background:#fff;padding:20px 28px 28px">
    <table style="border-collapse:collapse;width:100%">${tableRows}</table>
    <div style="margin-top:24px">
      <a href="tel:${escapeHtml(tel)}" style="display:inline-block;background:#0a0a0a;color:#fff;text-decoration:none;padding:12px 20px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;margin-right:8px">Call ${escapeHtml(lead.phone)}</a>
      <a href="mailto:${escapeHtml(lead.email)}" style="display:inline-block;border:1px solid #0a0a0a;color:#0a0a0a;text-decoration:none;padding:11px 20px;font-size:13px;letter-spacing:.14em;text-transform:uppercase">Reply by email</a>
    </div>
  </div>
  <div style="font-size:12px;color:#8c8c89;padding:16px 4px">Received ${new Date(inserted.created_at).toLocaleString("en-AU", { timeZone: "Australia/Sydney" })} (Sydney time).</div>
</div></body></html>`;

    const text = rows.filter(([, v]) => v).map(([k, v]) => `${k}: ${v}`).join("\n");
    const subjectBits = [lead.name, lead.service, lead.timeframe, lead.postcode ?? lead.suburb].filter(Boolean);

    try {
      const res = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
        body: JSON.stringify({
          from: FROM_EMAIL,
          to: [NOTIFY_EMAIL],
          reply_to: lead.email,
          subject: `New lead: ${subjectBits.join(" | ")}`,
          html,
          text,
        }),
      });
      emailSent = res.ok;
      if (!res.ok) console.error("Resend error", res.status, await res.text());
    } catch (e) {
      console.error("Resend request failed", e);
    }
  } else {
    console.error("RESEND_API_KEY is not set; lead stored without email.");
  }

  if (emailSent) {
    await supabase.from("leads").update({ email_sent: true }).eq("id", inserted.id);
  }

  return json({ ok: true, id: inserted.id });
});

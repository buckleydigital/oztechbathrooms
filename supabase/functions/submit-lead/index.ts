// submit-lead
// Receives quote requests from the website, stores them in public.leads
// and emails each one to the business via Resend.
//
// Saving and emailing are independent: if one fails, the other still runs,
// so a lead is never lost to a single problem. Every failure is logged with
// the reason (Supabase dashboard > Edge Functions > submit-lead > Logs).
//
// Secrets / env:
//   RESEND_API_KEY        (required) Resend API key
//   LEAD_NOTIFY_EMAIL     (optional) default info@oztechbathrooms.com.au
//   LEAD_FROM_EMAIL       (optional) default "OZTECH Bathrooms Website <onboarding@resend.dev>"
//                         Must be an address on a domain verified in Resend.
//                         Resend only delivers onboarding@resend.dev mail to the
//                         email address that owns the Resend account.
//   SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY are provided automatically.
//
// Health check (no secrets shown): open
//   https://<project>.supabase.co/functions/v1/submit-lead?check=1
//
// Deploy without JWT verification (the site calls it with the publishable key):
//   supabase functions deploy submit-lead --no-verify-jwt

import { createClient, type SupabaseClient } from "npm:@supabase/supabase-js@2.45.4";

const NOTIFY_EMAIL = (Deno.env.get("LEAD_NOTIFY_EMAIL") || "info@oztechbathrooms.com.au").trim();
const TEST_SENDER = "OZTECH Bathrooms Website <onboarding@resend.dev>";
const FROM_EMAIL = (Deno.env.get("LEAD_FROM_EMAIL") || TEST_SENDER).trim();

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}

function clean(v: unknown, max: number): string {
  if (typeof v !== "string") return "";
  return v.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "").trim().slice(0, max);
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

// Service key: the legacy service_role JWT, or a new-style secret key.
function serviceKey(): string | null {
  const legacy = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (legacy) return legacy;
  const keys = Deno.env.get("SUPABASE_SECRET_KEYS");
  if (keys) {
    try {
      const parsed = JSON.parse(keys);
      const first = typeof parsed === "object" && parsed ? Object.values(parsed)[0] : null;
      if (typeof first === "string" && first) return first;
    } catch { /* ignore */ }
  }
  return null;
}

function db(): SupabaseClient | null {
  const url = Deno.env.get("SUPABASE_URL");
  const key = serviceKey();
  if (!url || !key) {
    console.error("Database: SUPABASE_URL or service key is missing from the function environment.");
    return null;
  }
  return createClient(url, key, { auth: { persistSession: false } });
}

function senderDomain(from: string): string {
  const m = /@([^>\s]+)>?\s*$/.exec(from);
  return m ? m[1].toLowerCase() : "";
}

async function sendEmail(apiKey: string, from: string, payload: Record<string, unknown>) {
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
    body: JSON.stringify({ ...payload, from }),
  });
  const text = await res.text();
  return { ok: res.ok, status: res.status, body: text };
}

/* ------------------------------------------------------------------ */
/* Health check                                                        */
/* ------------------------------------------------------------------ */
async function healthCheck() {
  const apiKey = Deno.env.get("RESEND_API_KEY");
  const out: Record<string, unknown> = {
    resend_api_key_set: !!apiKey,
    sending_from: FROM_EMAIL,
    sending_to: NOTIFY_EMAIL,
    using_resend_test_sender: senderDomain(FROM_EMAIL) === "resend.dev",
    database_key_found: !!serviceKey(),
  };
  if (out.using_resend_test_sender) {
    out.warning = "onboarding@resend.dev only delivers to the email address that owns the Resend account. " +
      "Verify oztechbathrooms.com.au in Resend and set the LEAD_FROM_EMAIL secret.";
  }
  const client = db();
  if (client) {
    const { error } = await client.from("leads").select("id", { head: true, count: "exact" }).limit(1);
    out.database_ok = !error;
    if (error) out.database_error = error.message;
  }
  if (apiKey) {
    try {
      const res = await fetch("https://api.resend.com/domains", { headers: { Authorization: `Bearer ${apiKey}` } });
      if (res.ok) {
        const data = await res.json();
        const domains = (data.data || []).map((d: { name: string; status: string }) => ({ name: d.name, status: d.status }));
        out.resend_domains = domains;
        const want = senderDomain(FROM_EMAIL);
        if (want && want !== "resend.dev") {
          const match = domains.find((d: { name: string }) => d.name === want);
          out.sender_domain_status = match ? match.status : "not added to Resend";
        }
      } else {
        out.resend_domains = `Couldn't list domains (HTTP ${res.status}). A sending-only API key can't list domains; this is fine.`;
      }
    } catch (e) {
      out.resend_domains = `Couldn't reach Resend: ${e}`;
    }
  }
  return json(out);
}

/* ------------------------------------------------------------------ */
/* Handler                                                             */
/* ------------------------------------------------------------------ */
Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
  if (req.method === "GET" && new URL(req.url).searchParams.has("check")) return healthCheck();
  if (req.method !== "POST") return json({ error: "Method not allowed" }, 405);

  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return json({ error: "Invalid request." }, 400);
  }

  // Hidden spam-trap field. Bots fill it; real people never see it. Flagged
  // submissions are still saved (so a real lead is never lost to browser
  // autofill) but are labelled and not emailed.
  const flagged = !!clean(body.oz_hp, 200);
  if (flagged) console.log("Spam-trap field was filled; saving as flagged and not emailing.");

  const lead = {
    source: (clean(body.source, 40) || "website") + (flagged ? " (flagged as possible spam)" : ""),
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

  const client = db();

  // Flood protection: max 5 submissions per email per 10 minutes.
  if (client) {
    const since = new Date(Date.now() - 10 * 60 * 1000).toISOString();
    const { count, error } = await client
      .from("leads")
      .select("id", { count: "exact", head: true })
      .eq("email", lead.email)
      .gte("created_at", since);
    if (error) console.error("Flood check failed (continuing):", error.message);
    else if ((count ?? 0) >= 5) {
      console.log(`Flood limit hit for ${lead.email}`);
      return json({ error: "We've already received your enquiry. We'll be in touch shortly." }, 429);
    }
  }

  // 1) Save the lead
  let leadId: string | null = null;
  let receivedAt = new Date().toISOString();
  if (client) {
    const { data, error } = await client.from("leads").insert(lead).select("id, created_at").single();
    if (error) {
      console.error("Lead NOT saved to database:", error.message, error.details ?? "", error.hint ?? "");
    } else {
      leadId = data.id;
      receivedAt = data.created_at;
      console.log(`Lead saved: ${leadId}`);
    }
  }

  // 2) Email the lead (runs even if saving failed)
  let emailSent = false;
  const apiKey = Deno.env.get("RESEND_API_KEY");
  if (flagged) {
    // Not emailed; visible in the admin Leads tab.
  } else if (!apiKey) {
    console.error("Email NOT sent: the RESEND_API_KEY secret is not set for this function.");
  } else {
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
    const filled = rows.filter(([, v]) => v) as [string, string][];
    const tableRows = filled.map(([k, v]) =>
      `<tr><td style="padding:10px 16px 10px 0;color:#6b6b6b;font-size:13px;text-transform:uppercase;letter-spacing:.06em;vertical-align:top;white-space:nowrap">${k}</td>` +
      `<td style="padding:10px 0;font-size:15px;color:#0a0a0a;white-space:pre-wrap">${escapeHtml(v)}</td></tr>`
    ).join("");
    const tel = lead.phone.replace(/[^\d+]/g, "");
    const when = new Date(receivedAt).toLocaleString("en-AU", { timeZone: "Australia/Sydney" });
    const notSaved = leadId ? "" :
      `<div style="background:#fdf3f2;color:#7a1a12;padding:12px 16px;font-size:13px;margin-bottom:16px">This lead could not be saved to the admin area, so this email is the only copy. Please keep it.</div>`;
    const html = `<!doctype html><html><body style="margin:0;background:#f5f5f3;font-family:Helvetica,Arial,sans-serif">
<div style="max-width:600px;margin:0 auto;padding:32px 16px">
  <div style="background:#0a0a0a;color:#fff;padding:24px 28px">
    <div style="font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#b9b9b6">New website lead</div>
    <div style="font-size:24px;margin-top:8px;font-weight:bold">${escapeHtml(lead.name)}</div>
  </div>
  <div style="background:#fff;padding:20px 28px 28px">
    ${notSaved}
    <table style="border-collapse:collapse;width:100%">${tableRows}</table>
    <div style="margin-top:24px">
      <a href="tel:${escapeHtml(tel)}" style="display:inline-block;background:#0a0a0a;color:#fff;text-decoration:none;padding:12px 20px;font-size:14px;margin-right:8px">Call ${escapeHtml(lead.phone)}</a>
      <a href="mailto:${escapeHtml(lead.email)}" style="display:inline-block;border:1px solid #0a0a0a;color:#0a0a0a;text-decoration:none;padding:11px 20px;font-size:14px">Reply by email</a>
    </div>
  </div>
  <div style="font-size:12px;color:#8c8c89;padding:16px 4px">Received ${when} (Sydney time).</div>
</div></body></html>`;
    const text = (leadId ? "" : "NOTE: this lead could not be saved to the admin area. This email is the only copy.\n\n") +
      filled.map(([k, v]) => `${k}: ${v}`).join("\n") + `\n\nReceived ${when} (Sydney time).`;
    const subjectBits = [lead.name, lead.service, lead.timeframe, lead.postcode ?? lead.suburb].filter(Boolean);
    const payload = {
      to: [NOTIFY_EMAIL],
      reply_to: lead.email,
      subject: `New lead: ${subjectBits.join(" | ")}`,
      html,
      text,
    };

    try {
      let r = await sendEmail(apiKey, FROM_EMAIL, payload);
      if (r.ok) {
        emailSent = true;
        console.log(`Email sent to ${NOTIFY_EMAIL} from ${FROM_EMAIL}: ${r.body}`);
      } else {
        console.error(`Email NOT sent from ${FROM_EMAIL} to ${NOTIFY_EMAIL}. Resend said (HTTP ${r.status}): ${r.body}`);
        // If a custom sender failed (e.g. domain not verified yet), try Resend's test sender.
        if (FROM_EMAIL !== TEST_SENDER) {
          r = await sendEmail(apiKey, TEST_SENDER, payload);
          if (r.ok) {
            emailSent = true;
            console.log(`Email sent using the Resend test sender instead: ${r.body}`);
          } else {
            console.error(`Retry with the Resend test sender also failed (HTTP ${r.status}): ${r.body}`);
          }
        }
      }
    } catch (e) {
      console.error("Email NOT sent: couldn't reach Resend:", e);
    }
  }

  if (leadId && emailSent && client) {
    const { error } = await client.from("leads").update({ email_sent: true }).eq("id", leadId);
    if (error) console.error("Couldn't mark lead as emailed:", error.message);
  }

  if (flagged) return json({ ok: true });
  if (!leadId && !emailSent) {
    return json({ error: "Sorry, something went wrong sending your enquiry. Please call us instead." }, 500);
  }
  return json({ ok: true, id: leadId, saved: !!leadId, emailed: emailSent });
});

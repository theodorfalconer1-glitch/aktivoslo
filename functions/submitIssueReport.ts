import { createClientFromRequest } from 'npm:@base44/sdk@0.8.25';

export default async function handler(req: Request): Promise<Response> {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
  };

  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers });
  }

  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers,
    });
  }

  let body: Record<string, string>;
  try {
    body = await req.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
      status: 400,
      headers,
    });
  }

  const { place_id, place_name, issue_type, description } = body;

  if (!place_id || !place_name || !issue_type) {
    return new Response(
      JSON.stringify({ error: 'Mangler place_id, place_name eller issue_type' }),
      { status: 400, headers }
    );
  }

  const VALID_TYPES = [
    'feil_plassering',
    'feil_nettside',
    'feil_informasjon',
    'finnes_ikke',
    'annet',
  ];

  if (!VALID_TYPES.includes(issue_type)) {
    return new Response(
      JSON.stringify({ error: 'Ugyldig issue_type' }),
      { status: 400, headers }
    );
  }

  const safeDescription =
    typeof description === 'string'
      ? description.slice(0, 300).trim()
      : '';

  try {
    const base44 = createClientFromRequest(req);
    const db = base44.asServiceRole;

    const record = await db.entities.IssueReport.create({
      place_id: String(place_id).slice(0, 100),
      place_name: String(place_name).slice(0, 200),
      issue_type,
      description: safeDescription,
      reported_at: new Date().toISOString(),
      status: 'new',
    });

    return new Response(JSON.stringify({ ok: true, id: record.id }), {
      status: 201,
      headers,
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    console.error('IssueReport create error:', message);
    return new Response(
      JSON.stringify({ error: 'Klarte ikke lagre rapport', detail: message }),
      { status: 500, headers }
    );
  }
}

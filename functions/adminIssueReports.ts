import { createClientFromRequest } from 'npm:@base44/sdk@0.8.25';

export default async function handler(req: Request): Promise<Response> {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, PATCH, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Content-Type': 'application/json',
  };

  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers });
  }

  const base44 = createClientFromRequest(req);
  const db = base44.asServiceRole;

  // GET: hent alle rapporter
  if (req.method === 'GET') {
    try {
      const reports = await db.entities.IssueReport.list({ limit: 200 });
      // Sorter: nye først
      reports.sort((a: {reported_at?: string}, b: {reported_at?: string}) => {
        const ta = a.reported_at || '';
        const tb = b.reported_at || '';
        return tb.localeCompare(ta);
      });
      return new Response(JSON.stringify(reports), { status: 200, headers });
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      return new Response(JSON.stringify({ error: message }), { status: 500, headers });
    }
  }

  // PATCH: endre status (new → resolved)
  if (req.method === 'PATCH') {
    let body: { id: string; status: string };
    try {
      body = await req.json();
    } catch {
      return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400, headers });
    }

    const { id, status } = body;
    if (!id || !['new', 'resolved'].includes(status)) {
      return new Response(JSON.stringify({ error: 'Mangler id eller ugyldig status' }), {
        status: 400,
        headers,
      });
    }

    try {
      await db.entities.IssueReport.update(id, { status });
      return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      return new Response(JSON.stringify({ error: message }), { status: 500, headers });
    }
  }

  return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405, headers });
}

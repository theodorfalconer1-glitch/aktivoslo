import { createClientFromRequest } from 'npm:@base44/sdk@0.8.25';

Deno.serve(async (req) => {
  const cors = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  };
  if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });

  try {
    const base44 = createClientFromRequest(req);
    const body = await req.json().catch(() => ({}));
    const { action, token, data } = body;

    // Service-role client (no user auth needed for all ops)
    const db = base44.asServiceRole;

    async function getUser(uid: string) {
      if (!uid) return null;
      const users = await db.entities.User.filter({ id: uid });
      return users?.[0] || null;
    }

    // ── PING ──────────────────────────────────
    if (action === 'ping') {
      return Response.json({ ok: true }, { headers: cors });
    }

    // ── REGISTER ──────────────────────────────
    if (action === 'register') {
      const { email, password, display_name, avatar_emoji } = data || {};
      if (!email || !password || !display_name) {
        return Response.json({ error: 'Mangler felt' }, { status: 400, headers: cors });
      }
      const existing = await db.entities.User.filter({ email });
      if (existing?.length) {
        return Response.json({ error: 'E-post allerede i bruk' }, { status: 409, headers: cors });
      }
      const pw_hash = btoa(unescape(encodeURIComponent(password + 'ao2025')));
      const user = await db.entities.User.create({
        email, pw_hash, display_name,
        avatar_emoji: avatar_emoji || '🏃',
        role: 'user', friend_ids: [],
        visited_places: [], saved_places: [], streak_count: 0,
      });
      const { pw_hash: _, ...safe } = user;
      return Response.json({ ok: true, user: safe }, { headers: cors });
    }

    // ── LOGIN ─────────────────────────────────
    if (action === 'login') {
      const { email, password } = data || {};
      if (!email || !password) {
        return Response.json({ error: 'Mangler felt' }, { status: 400, headers: cors });
      }
      const users = await db.entities.User.filter({ email });
      const user = users?.[0];
      if (!user) return Response.json({ error: 'Finner ikke bruker' }, { status: 404, headers: cors });
      const pw_hash = btoa(unescape(encodeURIComponent(password + 'ao2025')));
      if (user.pw_hash !== pw_hash) {
        return Response.json({ error: 'Feil passord' }, { status: 401, headers: cors });
      }
      const { pw_hash: _, ...safe } = user;
      return Response.json({ ok: true, user: safe }, { headers: cors });
    }

    // ── AUTH CHECK ────────────────────────────
    if (!token) {
      return Response.json({ error: 'Ikke innlogget' }, { status: 401, headers: cors });
    }
    const me = await getUser(token);
    if (!me) return Response.json({ error: 'Ugyldig token' }, { status: 401, headers: cors });

    // ── SYNC PROGRESS ─────────────────────────
    if (action === 'sync_progress') {
      const { visited_places, saved_places, streak_count, streak_last_date } = data || {};
      await db.entities.User.update(me.id, {
        ...(visited_places !== undefined && { visited_places }),
        ...(saved_places !== undefined && { saved_places }),
        ...(streak_count !== undefined && { streak_count }),
        ...(streak_last_date && { streak_last_date }),
      });
      return Response.json({ ok: true }, { headers: cors });
    }

    // ── UPDATE PROFILE ────────────────────────
    if (action === 'update_profile') {
      const { display_name, avatar_emoji, bio, favorite_types } = data || {};
      const updated = await db.entities.User.update(me.id, {
        ...(display_name && { display_name }),
        ...(avatar_emoji && { avatar_emoji }),
        ...(bio !== undefined && { bio }),
        ...(favorite_types && { favorite_types }),
      });
      const { pw_hash: _, ...safe } = updated;
      return Response.json({ ok: true, user: safe }, { headers: cors });
    }

    // ── SEARCH USERS ──────────────────────────
    if (action === 'search_users') {
      const { query } = data || {};
      if (!query || query.length < 2) return Response.json({ users: [] }, { headers: cors });
      const all = await db.entities.User.list();
      const matches = (all || [])
        .filter((u: any) => u.id !== me.id && u.display_name?.toLowerCase().includes(query.toLowerCase()))
        .slice(0, 8)
        .map((u: any) => ({ id: u.id, display_name: u.display_name, avatar_emoji: u.avatar_emoji, bio: u.bio || '' }));
      return Response.json({ users: matches }, { headers: cors });
    }

    // ── SEND FRIEND REQUEST ───────────────────
    if (action === 'send_friend_request') {
      const { to_user_id } = data || {};
      if (!to_user_id) return Response.json({ error: 'Mangler bruker-id' }, { status: 400, headers: cors });
      if ((me.friend_ids || []).includes(to_user_id)) {
        return Response.json({ error: 'Allerede venner' }, { status: 409, headers: cors });
      }
      const existing = await db.entities.FriendRequest.filter({ from_user_id: me.id, to_user_id, status: 'pending' });
      if (existing?.length) return Response.json({ error: 'Allerede sendt' }, { status: 409, headers: cors });
      await db.entities.FriendRequest.create({
        from_user_id: me.id, from_display_name: me.display_name, to_user_id, status: 'pending',
      });
      return Response.json({ ok: true }, { headers: cors });
    }

    // ── GET FRIEND REQUESTS ───────────────────
    if (action === 'get_friend_requests') {
      const reqs = await db.entities.FriendRequest.filter({ to_user_id: me.id, status: 'pending' });
      return Response.json({ requests: reqs || [] }, { headers: cors });
    }

    // ── RESPOND FRIEND REQUEST ────────────────
    if (action === 'respond_friend_request') {
      const { request_id, accept } = data || {};
      const reqs = await db.entities.FriendRequest.filter({ id: request_id });
      const reqItem = reqs?.[0];
      if (!reqItem || reqItem.to_user_id !== me.id) {
        return Response.json({ error: 'Ikke funnet' }, { status: 404, headers: cors });
      }
      await db.entities.FriendRequest.update(request_id, { status: accept ? 'accepted' : 'declined' });
      if (accept) {
        const from = await getUser(reqItem.from_user_id);
        await db.entities.User.update(me.id, {
          friend_ids: [...new Set([...(me.friend_ids || []), reqItem.from_user_id])],
        });
        if (from) {
          await db.entities.User.update(from.id, {
            friend_ids: [...new Set([...(from.friend_ids || []), me.id])],
          });
        }
      }
      return Response.json({ ok: true }, { headers: cors });
    }

    // ── GET FRIENDS ───────────────────────────
    if (action === 'get_friends') {
      const ids = me.friend_ids || [];
      const friends = await Promise.all(ids.map((id: string) => getUser(id)));
      const safe = friends.filter(Boolean).map((u: any) => ({
        id: u.id, display_name: u.display_name, avatar_emoji: u.avatar_emoji,
        bio: u.bio || '', visited_count: (u.visited_places || []).length,
      }));
      return Response.json({ friends: safe }, { headers: cors });
    }

    // ── CREATE GROUP ──────────────────────────
    if (action === 'create_group') {
      const { name, emoji } = data || {};
      if (!name) return Response.json({ error: 'Mangler navn' }, { status: 400, headers: cors });
      const invite_code = Math.random().toString(36).slice(2, 8).toUpperCase();
      const group = await db.entities.Group.create({
        name, emoji: emoji || '👥', created_by: me.id,
        member_ids: [me.id], invite_code, plans: [],
      });
      return Response.json({ ok: true, group }, { headers: cors });
    }

    // ── JOIN GROUP ────────────────────────────
    if (action === 'join_group') {
      const { invite_code } = data || {};
      const groups = await db.entities.Group.filter({ invite_code });
      const group = groups?.[0];
      if (!group) return Response.json({ error: 'Finner ikke gruppe (sjekk koden)' }, { status: 404, headers: cors });
      if ((group.member_ids || []).includes(me.id)) {
        return Response.json({ error: 'Du er allerede med' }, { status: 409, headers: cors });
      }
      const updated = await db.entities.Group.update(group.id, {
        member_ids: [...(group.member_ids || []), me.id],
      });
      return Response.json({ ok: true, group: updated }, { headers: cors });
    }

    // ── GET MY GROUPS ─────────────────────────
    if (action === 'get_my_groups') {
      const all = await db.entities.Group.list();
      const mine = (all || []).filter((g: any) => (g.member_ids || []).includes(me.id));
      return Response.json({ groups: mine }, { headers: cors });
    }

    // ── GET GROUP (with members) ───────────────
    if (action === 'get_group') {
      const { group_id } = data || {};
      const groups = await db.entities.Group.filter({ id: group_id });
      const group = groups?.[0];
      if (!group || !(group.member_ids || []).includes(me.id)) {
        return Response.json({ error: 'Ikke tilgang' }, { status: 403, headers: cors });
      }
      const members = await Promise.all((group.member_ids || []).map((id: string) => getUser(id)));
      const safeMembers = members.filter(Boolean).map((u: any) => ({
        id: u.id, display_name: u.display_name, avatar_emoji: u.avatar_emoji,
        visited_count: (u.visited_places || []).length,
      }));
      return Response.json({ group: { ...group, members: safeMembers } }, { headers: cors });
    }

    // ── SUGGEST PLAN ──────────────────────────
    if (action === 'suggest_plan') {
      const { group_id, place_id, place_name, place_emoji, suggested_date, note } = data || {};
      const groups = await db.entities.Group.filter({ id: group_id });
      const group = groups?.[0];
      if (!group || !(group.member_ids || []).includes(me.id)) {
        return Response.json({ error: 'Ikke tilgang' }, { status: 403, headers: cors });
      }
      const plan = {
        id: Date.now().toString(36),
        place_id, place_name, place_emoji: place_emoji || '📍',
        suggested_by: me.id, suggested_by_name: me.display_name,
        suggested_date: suggested_date || null,
        note: note || '',
        votes_yes: [me.id], votes_no: [],
        created_at: new Date().toISOString(),
      };
      await db.entities.Group.update(group_id, {
        plans: [...(group.plans || []), plan],
      });
      return Response.json({ ok: true, plan }, { headers: cors });
    }

    // ── VOTE PLAN ─────────────────────────────
    if (action === 'vote_plan') {
      const { group_id, plan_id, vote } = data || {};
      const groups = await db.entities.Group.filter({ id: group_id });
      const group = groups?.[0];
      if (!group || !(group.member_ids || []).includes(me.id)) {
        return Response.json({ error: 'Ikke tilgang' }, { status: 403, headers: cors });
      }
      const plans = (group.plans || []).map((p: any) => {
        if (p.id !== plan_id) return p;
        const yes = (p.votes_yes || []).filter((id: string) => id !== me.id);
        const no = (p.votes_no || []).filter((id: string) => id !== me.id);
        if (vote === 'yes') yes.push(me.id);
        else no.push(me.id);
        return { ...p, votes_yes: yes, votes_no: no };
      });
      await db.entities.Group.update(group_id, { plans });
      return Response.json({ ok: true }, { headers: cors });
    }

    return Response.json({ error: 'Ukjent handling: ' + action }, { status: 400, headers: cors });

  } catch (err: any) {
    return Response.json({ error: err?.message || 'Serverfeil' }, { status: 500, headers: { 'Access-Control-Allow-Origin': '*' } });
  }
});

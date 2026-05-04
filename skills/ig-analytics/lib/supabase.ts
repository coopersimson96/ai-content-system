import { createClient, type SupabaseClient } from "@supabase/supabase-js";

let cached: SupabaseClient | null = null;

/**
 * Server-side Supabase client. Uses service role key (bypasses RLS) - only
 * import from server code (route handlers, scripts), never from client
 * components.
 *
 * Returns null if env vars are missing so handlers can fail gracefully with
 * a clear log line instead of throwing during module initialization.
 */
export function getSupabaseAdmin(): SupabaseClient | null {
  if (cached) return cached;

  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;

  if (!url || !key) {
    console.warn(
      "[supabase] SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY missing - admin client unavailable",
    );
    return null;
  }

  cached = createClient(url, key, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
  return cached;
}

# Module 1 — Supabase Auth and database foundation

## Implemented

- The browser Supabase client stores its session in cookies. Register and login use Supabase email/password Auth; dashboard logout uses the SDK. The dashboard listens for Auth state changes, including token refresh, and calls FastAPI with the current access token.
- Registration uses Supabase email/password Auth. The app does not request or process confirmation emails. The hosted project's own Auth settings determine whether signup returns an immediate session.
- FastAPI `GET /api/v1/auth/me` verifies a Bearer token against the configured project's JWKS, including signature, expiry, issuer, audience, authenticated role, and UUID subject. Invalid tokens return 401. An unavailable key service returns 503.
- SQLAlchemy creates a TLS-required PostgreSQL connection pool. `python -m scripts.check_database` runs a read-only connection check.

## Hosted project setup

1. In the Supabase dashboard, enable email/password under Authentication → Providers → Email. Confirmation email and custom SMTP setup are deferred until requested separately.
2. Under Authentication → URL Configuration, set the site URL to `http://localhost:3000` for local development. Use your real frontend origin for deployment.
3. Copy the repository `.env.example` to `.env`. Set `SUPABASE_URL` to the project URL, `DATABASE_URL` to the direct or session-pooler PostgreSQL connection string from the Supabase Connect dialog, and `FRONTEND_ORIGIN` to the frontend origin. Keep the database password only in the backend environment.
4. Create `frontend/.env.local` with `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` (the project's publishable key or legacy anon key), and `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`. Restart both apps after editing env files.
5. Use asymmetric JWT signing keys in the Supabase project. The FastAPI verifier intentionally accepts ES256 and RS256 public-key tokens from that project's JWKS; it does not accept legacy HS256 access tokens. Supabase's signing-key settings show which algorithm is active.

Use a direct or session-pooler database URL for this persistent FastAPI process. Transaction pooling needs prepared statements disabled and has session-state limitations; that mode is not configured here.

## Verify with a real project

From `backend`, run `python -m scripts.check_database`. Start the API and frontend, sign in with an existing active user, and confirm the dashboard shows the authenticated email/ID. In browser developer tools, confirm that `GET /api/v1/auth/me` returns 200 after login and 401 without a Bearer token. Reload the dashboard and sign out to check cookie persistence and session handling. Repeat after token refresh if the project has a short JWT lifetime. Registration can be tested independently; an immediate session depends on the hosted project's Auth settings.

Credentials belong only in ignored local env files. Unit/API tests use generated test signing keys and do not claim hosted-project verification.

## Hosted verification (2026-10-02)

- The configured Supabase project is active, and its PostgreSQL database answered a read-only `SELECT 1` through the Supabase connection.
- The direct database endpoint is IPv6-only from this development machine. The ignored local `DATABASE_URL` now uses the project's working IPv4 Session pooler; `python -m scripts.check_database` passed through the application's SQLAlchemy connection.
- The project's JWKS exposes an ES256 public signing key. FastAPI `/api/v1/auth/me` returned 401 for a missing token and for a forged token using the project's real JWKS.
- A 200 response with a real user token and the browser sign-in flow remain unverified because the project has no users yet. Confirmation email and SMTP setup are deferred.

## RLS boundary for Module 2

Supabase Auth owns `auth.users`. Module 2 creates application tables. For each table exposed directly through Supabase, enable RLS and add `authenticated` policies that compare indexed ownership columns against `(select auth.uid())`, with `WITH CHECK` for writes. Tables without a direct `user_id` need a parent ownership check. The backend PostgreSQL connection may use a privileged database role, so FastAPI must independently filter and verify ownership on every operation. No permissive table policy is created before the schema exists.

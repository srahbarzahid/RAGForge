# Module 1 — Supabase Auth and database foundation

## Implemented

- The browser Supabase client stores its session in cookies. Register and login use Supabase email/password Auth; dashboard logout uses the SDK. The dashboard listens for Auth state changes, including token refresh, and calls FastAPI with the current access token.
- Registration creates a session immediately when Supabase's Confirm Email setting is disabled. The app does not request or process confirmation emails.
- FastAPI `GET /api/v1/auth/me` verifies a Bearer token against the configured project's JWKS, including signature, expiry, issuer, audience, authenticated role, and UUID subject. Invalid tokens return 401. An unavailable key service returns 503.
- SQLAlchemy creates a TLS-required PostgreSQL connection pool. `python -m scripts.check_database` runs a read-only connection check.

## Hosted project setup

1. In the Supabase dashboard, enable email/password under Authentication → Providers → Email and **disable Confirm Email**. This is a project setting; the app cannot change it with the publishable key. Users can then register and receive a session immediately. Custom SMTP can be configured later.
2. Under Authentication → URL Configuration, set the site URL to `http://localhost:3000` for local development. Use your real frontend origin for deployment.
3. Copy the repository `.env.example` to `.env`. Set `SUPABASE_URL` to the project URL, `DATABASE_URL` to the direct or session-pooler PostgreSQL connection string from the Supabase Connect dialog, and `FRONTEND_ORIGIN` to the frontend origin. Keep the database password only in the backend environment.
4. Create `frontend/.env.local` with `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` (the project's publishable key or legacy anon key), and `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`. Restart both apps after editing env files.
5. Use asymmetric JWT signing keys in the Supabase project. The FastAPI verifier intentionally accepts ES256 and RS256 public-key tokens from that project's JWKS; it does not accept legacy HS256 access tokens. Supabase's signing-key settings show which algorithm is active.

Use a direct or session-pooler database URL for this persistent FastAPI process. Transaction pooling needs prepared statements disabled and has session-state limitations; that mode is not configured here.

## Verify with a real project

From `backend`, run `python -m scripts.check_database`. Start the API and frontend, register an account, and confirm that signup opens the dashboard immediately without an email step. Sign out and back in. The dashboard should show the authenticated email/ID. In browser developer tools, confirm that `GET /api/v1/auth/me` returns 200 after login and 401 without a Bearer token. Reload the dashboard and sign out to check cookie persistence and session handling. Repeat after token refresh if the project has a short JWT lifetime.

Credentials belong only in ignored local env files. Unit/API tests use generated test signing keys and do not claim hosted-project verification.

## RLS boundary for Module 2

Supabase Auth owns `auth.users`. Module 2 creates application tables. For each table exposed directly through Supabase, enable RLS and add `authenticated` policies that compare indexed ownership columns against `(select auth.uid())`, with `WITH CHECK` for writes. Tables without a direct `user_id` need a parent ownership check. The backend PostgreSQL connection may use a privileged database role, so FastAPI must independently filter and verify ownership on every operation. No permissive table policy is created before the schema exists.

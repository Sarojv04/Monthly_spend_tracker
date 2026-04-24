# Spec: Login and Logout

## Overview
Implement session-based authentication so registered users can sign in to Spendly and sign out. This step upgrades the stub `GET /login` route into a fully functional `POST /login` handler that verifies credentials, stores the user in a Flask session, and redirects on success. The `GET /logout` stub is replaced with a handler that clears the session and redirects to the landing page. The navbar in `base.html` is updated to conditionally display the user's name and a Sign out link when logged in, or Sign in / Get started links when not logged in.

## Depends on
- Step 01 – Database Setup (`database/db.py` with `get_db`, `get_user_by_email`, `users` table in schema)
- Step 02 – Registration (users exist in the database; `app.secret_key` already set; `base.html` and `login.html` already created)

## Routes
- `GET  /login` — render login form — public (already exists, no changes needed)
- `POST /login` — validate email and password, set session, redirect to `/` on success or re-render form with error — public
- `GET  /logout` — clear the session, redirect to `/` — public (safe to call even if not logged in)

## Database changes
No new tables or columns.

One new helper function must be added to `database/db.py`:

- `get_user_by_id(user_id)` — returns a `sqlite3.Row` for the matching user or `None`. Must use a parameterised query.

## Templates
- **Create:** none
- **Modify:** `templates/base.html` — update the `<nav>` links block to conditionally render:
  - If `session.user_id` is set: show the logged-in user's name (from `session['user_name']`) and a `Sign out` link pointing to `/logout`
  - If no session: show existing `Sign in` and `Get started` links

## Files to change
- `app.py` — add `session` and `check_password_hash` imports; implement `POST /login` handler; implement `GET /logout` handler; import `get_user_by_id`
- `database/db.py` — add `get_user_by_id(user_id)`
- `templates/base.html` — update navbar to be session-aware

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings or `%` formatting in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Session keys to store on login: `session['user_id']` (integer) and `session['user_name']` (string)
- On login failure, re-render `login.html` with an `error` variable — do **not** redirect
- Login validation order:
  1. Email field present and non-empty
  2. Password field present and non-empty
  3. User exists for that email
  4. Password matches the stored hash
- Use a single generic error message for steps 3 and 4 ("Invalid email or password") — do not reveal which check failed
- `GET /logout` must call `session.clear()`, then redirect to `/` with HTTP 302
- After successful login, redirect to `/` with HTTP 302 (dashboard redirect will be updated in a later step)

## Definition of done
- [ ] `GET /login` renders the login form without errors
- [ ] Submitting valid email and password sets the session and redirects to `/`
- [ ] Submitting an unregistered email re-renders the form with an error message (no redirect)
- [ ] Submitting a wrong password for a valid email re-renders the form with an error message (no redirect)
- [ ] Submitting with any field empty re-renders the form with an error message (no redirect)
- [ ] After login, the navbar shows the user's name and a Sign out link instead of Sign in / Get started
- [ ] Visiting `/logout` clears the session and redirects to `/`
- [ ] After logout, the navbar shows Sign in / Get started again
- [ ] The app starts without errors (`python app.py`)
- [ ] Refreshing any page after login keeps the user logged in (session persists across requests)

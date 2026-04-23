# Spec: Registration

## Overview
## Overview

Implement user registration so new visitors can create a Spendly account. This step upgrades the existing stub `GET /register` route into a fully functional form that accepts a POST, validates input, hashes the password, and inserts a new row into the `users` table. On success the user is shown with a success message and then redirected to the login page. This is the entry point for all authenticated features that follow.

## Depends on
- Step 01 – Database Setup (`database/db.py` with `init_db`, `seed_db`, `get_db` already implemented and the `users` table already in schema)

## Routes
- `GET  /register` – render registration form – public (already exists, no changes needed)
- `POST /register` – validate form data, create user, redirect to login – public

## Database changes
No new tables. Two new helper functions must be added to `database/db.py`:

- `create_user(name, email, password_hash)` — inserts a row into `users`, returns the new `id`
- `get_user_by_email(email)` — returns a `sqlite3.Row` for the matching user or `None`

Both must use parameterised queries. No raw string interpolation in SQL.

## Templates
- **Create:** `templates/base.html` — shared layout (navbar, `<main>` block, footer). All existing and future templates extend this file. Must use CSS variables only; no hardcoded hex values. Must link `static/css/style.css` and `static/js/main.js`.
- **Modify:** none — `templates/register.html` already has the correct form markup and error block; leave it untouched unless a bug is found.

## Files to change
- `app.py` — add `app.secret_key`, import `create_user` and `get_user_by_email`, implement `POST /register` handler
- `database/db.py` — add `create_user()` and `get_user_by_email()`

## Files to create
- `templates/base.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings or `%` formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` before insert; never store plaintext
- Use CSS variables — never hardcode hex values in `base.html`
- All templates extend `base.html`
- `secret_key` must be set on the Flask app (required for sessions in later steps); use a hard-coded dev string for now
- POST /register validation order:
  1. All fields present and non-empty
  2. Password is at least 8 characters
  3. Email not already registered (query DB)
- On any validation failure, re-render `register.html` with an `error` variable — do **not** redirect
- On success, redirect to `/login` with HTTP 302

## Definition of done
- [ ] `GET /register` renders the registration form without errors
- [ ] Submitting valid name, email, and password (≥ 8 chars) inserts a new row into `users` and redirects to `/login`
- [ ] Submitting a duplicate email re-renders the form with an error message (no redirect)
- [ ] Submitting a password shorter than 8 characters re-renders the form with an error message
- [ ] Submitting with any field empty re-renders the form with an error message
- [ ] The stored `password_hash` in the database is not equal to the plaintext password
- [ ] `base.html` renders the Spendly navbar and footer visible on the `/register` page
- [ ] The app starts without errors (`python app.py`)

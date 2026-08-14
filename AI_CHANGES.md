# AI_CHANGES.md

This file documents every contribution made to this repository by AI coding agents.

## Instructions for future agents

When you modify this repository, you MUST keep this file up to date:

1. Add an entry for **every** change you make (backend and frontend), including bug fixes,
   new features, refactors, and documentation.
2. Separate your entries by the sections below: **Backend** and **Frontend**.
3. For each entry include:
   - A one-line description of the change.
   - The files touched (relative paths).
   - The reason it was needed (e.g. bug fix, new feature request).
4. Keep the most recent entry at the **top** of its section, above older entries.
5. Do not remove or rewrite historical entries — append only.

## Backend

### 2026-08-14 — Fix database connection leaks
- All functions in `database.py` now open connections with `with sqlite3.connect(...)` context
  managers instead of leaving connections/transactions open.
- Reason: when a query raised (e.g. UNIQUE constraint), sqlite left an uncommitted write
  transaction open on the never-closed connection, locking the database for all subsequent
  writes (`sqlite3.OperationalError: database is locked`).

### 2026-08-14 — SQL injection hardening
- Parameterized all user-supplied values in `database.py` queries (`insert_user`, `retrieve_user`,
  `remove_user`, `change_user`, `insert_admin`, `retrieve_admin`, `remove_admin`) using `?`
  placeholders instead of f-string interpolation.
- Restricted `change_user()` column names to a fixed allow-list (`name`, `age`, `gender`, `role`,
  `salary`), raising `ValueError` otherwise.
- Fixed `retrieve_admin()` selecting from the `users` table instead of `admins` in its `id` branch.
- Reason: queries were directly interpolating user input (SQL injection); the id branch returned
  the wrong records.

### 2026-08-14 — Robust static file path
- `main.py` now resolves `static/index.html` relative to the module location via
  `Path(__file__).parent` instead of a CWD-relative string.
- Reason: `GET /` broke when the server was started from a different working directory.

### 2026-08-14 — Delete-admin bug fix
- Fixed `remove_admin()` in `database.py` deleting from the `users` table instead of the
  `admins` table.
- Fixed `delete_admin()` in `main.py` referencing an undefined `id` variable in its log line.
- Reason: admin deletion returned a 500 error and removed the wrong records.

### 2026-08-14 — Serve web UI from the root route
- `main.py` now serves `static/index.html` at `GET /` via `FileResponse` (replacing the previous
  trivial JSON response).
- Reason: provide a single entry point for the web console without CORS setup.

## Frontend

### 2026-08-14 — Hide delete button for the only remaining admin
- `loadAdmins()` in `static/index.html` now renders the per-row Delete button only when the
  admin list has more than one entry, leaving an empty actions cell otherwise.
- Reason: mirror the backend guard in `main.py` that rejects deleting the sole admin (405), so
  users are not presented with an action the API will refuse.

### 2026-08-14 — XSS hardening & cleanup
- Replaced inline `onclick` handlers in `static/index.html` with event delegation: buttons now carry
  `data-action`/`data-id`/`data-name` attributes and clicks are handled by `addEventListener` on the
  table containers. The admin delete button previously interpolated the username directly into a JS
  string literal, allowing stored XSS via a malicious username.
- Removed the unused `urlWithKey()` helper.
- Reason: a username containing a quote could escape the inline JS string literal and execute
  arbitrary code when the console was loaded.

### 2026-08-14 — Web console UI (new)
- Added `static/index.html`: a single-page, dependency-free web interface for the API.
- Features:
  - Login via `GET /authenticate` (HTTP Basic), storing the returned API key in `sessionStorage`
    with a live 10-minute expiry countdown and logout.
  - Users section: list, create, inline edit, and delete users.
  - Admins section: list, add, and delete admins.
  - Status/error banner that prompts re-login when the API returns 401.
- Reason: provide a simple web interface to access the pyapi backend.

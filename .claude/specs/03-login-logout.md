# Spec: Login and Logout

## Overview
This feature implements the authentication mechanism for Spendly. It allows users to securely log into their accounts using their email and password, and to securely log out. This is a critical step in the roadmap as it establishes the session management required for all subsequent personalized features (Profile, Expense Tracking, etc.).

## Depends on
- 02 Registration

## Routes
- `GET /login` — Display login form — public
- `POST /login` — Authenticate user and start session — public
- `GET /logout` — Terminate session and redirect to landing — logged-in

## Database changes
No database changes.

## Templates
- **Modify:** `templates/login.html` — Add form fields (email, password) and submit button.
- **Modify:** `templates/base.html` — Add conditional navigation links (Login/Logout) based on session state.

## Files to change
- `app.py` — Implement logic for `/login` (POST) and `/logout`.
- `templates/login.html` — Update for actual form submission.
- `templates/base.html` — Update navigation for auth state.

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use Flask `session` for user state management.

## Definition of done
- [ ] User can navigate to `/login` and see the form.
- [ ] User can log in with valid credentials and be redirected to a protected page (e.g., `/profile`).
- [ ] User sees an error message when attempting to log in with an invalid email or password.
- [ ] User can log out via `/logout`, which clears the session and redirects to the landing page.
- [ ] Navigation menu in `base.html` correctly toggles between "Login" and "Logout" based on auth status.

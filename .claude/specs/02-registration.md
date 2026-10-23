# Spec: Registration

## Overview
This feature implements the user registration process, allowing new users to create an account. This is a critical second step in the roadmap to enable authenticated access to the expense tracker.

## Depends on
- 01-database-setup

## Routes
- `GET /register` — Display the registration form — public
- `POST /register` — Handle user registration and account creation — public

## Database changes
No database changes. The `users` table was created in Step 01 with necessary fields (`name`, `email`, `password_hash`, `created_at`).

## Templates
- **Create:** None (Existing `register.html` is present but needs to be functional)
- **Modify:** `templates/register.html` — Update to use a proper HTML form that posts to `/register`.

## Files to change
- `app.py` — Implement the `POST /register` route and validation logic.

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

## Definition of done
- User can navigate to `/register`.
- User can submit the registration form with name, email, and password.
- Form validation prevents duplicate emails from being registered.
- Successfully registered users are redirected to the login page or a success page.
- New users are correctly inserted into the `users` table with hashed passwords.

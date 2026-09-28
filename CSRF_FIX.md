# CSRF Fix — Krishi-Sahayak

## Objective

Fix the existing CSRF protection issues identified during the project analysis.

The application must keep CSRF protection enabled. Do NOT disable, bypass, or weaken CSRF protection.

## Task 1: Inspect Current CSRF Implementation

Inspect `app.py` and determine exactly how CSRF protection is implemented.

Identify all POST, PUT, and DELETE routes that require CSRF protection.

## Task 2: Find Missing CSRF Tokens

Inspect all templates and JavaScript files for forms and AJAX/fetch requests that perform POST, PUT, or DELETE operations.

Identify requests that currently do not provide the required CSRF token.

## Task 3: Fix CSRF Handling

Add the correct CSRF token handling to the affected forms and JavaScript requests.

Use the existing CSRF implementation and follow the project's current architecture.

Do not create a second CSRF system.

Do not disable CSRF validation.

Do not hard-code CSRF tokens.

## Task 4: Verify

Run appropriate read-only/static checks and relevant tests.

Confirm that:

- Existing login functionality still works.
- Affected forms include CSRF protection.
- Affected AJAX requests include CSRF protection.
- CSRF protection remains enabled.
- No unrelated functionality is changed.

## Task 5: Report

Summarize:

- Files changed
- What was fixed
- Tests/checks performed
- Any remaining CSRF-related issues

Only make changes necessary for this CSRF fix.
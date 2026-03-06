# IliadPublicCDN

> ⚠️ **PUBLIC REPOSITORY — DO NOT COMMIT SENSITIVE FILES**

This repository hosts **public-facing assets only** (images, fonts, scripts, stylesheets, and other static resources) served via the Iliad CDN.

## ‼️ What does NOT belong here

The following must **never** be committed to this repository:

- Environment files (`.env`, `.env.*`)
- Credentials, API keys, or auth tokens (`credentials.json`, `service-account*.json`, `*.key`, `*.pem`, etc.)
- Private certificates or SSH keys
- Firebase / Google Cloud service-account files (`firebase-adminsdk*.json`, `google-services.json`)
- AWS config or credential files
- Database dumps, backups, or exports
- Log files that may contain sensitive data
- Any file containing passwords, secrets, or personally identifiable information (PII)

A `.gitignore` is in place to help catch common sensitive file patterns, but it is **not a substitute for human review**. Always inspect your staged files with `git diff --staged` before committing.

## ✅ What belongs here

- Static images, icons, and media assets
- Public fonts
- Publicly distributable JavaScript/CSS bundles
- Other files that are **safe to serve publicly without authentication**

## Reporting accidental exposure

If a sensitive file was committed, treat the secret as compromised immediately:

1. Rotate / revoke the exposed credential.
2. Remove the file from git history using `git filter-repo` or BFG Repo Cleaner.
3. Force-push the cleaned history and notify the team.

For questions, contact the Iliad development team.

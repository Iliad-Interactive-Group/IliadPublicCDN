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
Public asset CDN hosted on GitHub Pages. Upload images, logos, JSON, fonts, and other files — then reference them by URL anywhere.

## 🌐 Live Site

**CDN Root:** `https://iliad-interactive-group.github.io/IliadPublicCDN/`

**Admin Panel:** `https://iliad-interactive-group.github.io/IliadPublicCDN/admin/`

## 📁 Folder Structure

| Folder     | Purpose               | Example URL |
|------------|----------------------|-------------|
| `images/`  | General images        | `.../images/hero.png` |
| `logos/`   | Brand logos & icons    | `.../logos/logo.svg` |
| `files/`   | JSON, PDF, documents  | `.../files/config.json` |
| `fonts/`   | Web fonts             | `.../fonts/custom.woff2` |
| `videos/`  | Video files           | `.../videos/intro.mp4` |

## 🚀 Usage

### Reference a file in your code

```html
<img src="https://iliad-interactive-group.github.io/IliadPublicCDN/logos/logo.png" alt="Logo">
```

```css
@font-face {
  font-family: 'CustomFont';
  src: url('https://iliad-interactive-group.github.io/IliadPublicCDN/fonts/custom.woff2');
}
```

```ts
const config = await fetch('https://iliad-interactive-group.github.io/IliadPublicCDN/files/config.json')
```

### Adding files

**Option 1 — Admin Panel (recommended)**

1. Go to the [Admin Panel](https://iliad-interactive-group.github.io/IliadPublicCDN/admin/)
2. Enter a GitHub PAT with `repo` or `contents:write` permission
3. Select a folder, drag-and-drop files, and upload
4. Copy the served URL shown after upload

**Option 2 — Git**

1. Add files to the appropriate folder (`images/`, `logos/`, etc.)
2. Commit and push to `main`
3. GitHub Actions will rebuild and deploy to Pages automatically

## ⚙️ How It Works

- Files live in categorized folders at the repo root
- A Python build script (`scripts/build.py`) generates HTML index pages for browsing
- GitHub Actions deploys everything to GitHub Pages on push to `main`
- The admin panel uses the GitHub API client-side to upload files directly to the repo

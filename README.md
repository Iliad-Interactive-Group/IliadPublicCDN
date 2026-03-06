# IliadPublicCDN

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

#!/usr/bin/env python3
"""
Build script for IliadPublicCDN.

Scans the CDN asset directories and generates:
  - A root index.html landing page with links to each category
  - Per-directory index.html pages with file grids (image previews, file links)

All output goes into the _site/ directory, which is then deployed to GitHub Pages.
"""

import os
import shutil
import html
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = REPO_ROOT / "_site"
BASE_URL = ""  # relative paths work for GitHub Pages

ASSET_DIRS = ["images", "logos", "files", "fonts", "videos"]

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".bmp", ".avif"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogg", ".mov"}
FONT_EXTENSIONS = {".woff", ".woff2", ".ttf", ".otf", ".eot"}

EXCLUDED_FILES = {".gitkeep", ".DS_Store", "Thumbs.db", "index.html"}


def get_file_size(path: Path) -> str:
    size = path.stat().st_size
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}" if unit != "B" else f"{size} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def is_image(filename: str) -> bool:
    return Path(filename).suffix.lower() in IMAGE_EXTENSIONS


def is_video(filename: str) -> bool:
    return Path(filename).suffix.lower() in VIDEO_EXTENSIONS


def html_head(title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📦</text></svg>">
</head>"""


def build_landing_page(categories: dict[str, list[str]]) -> str:
    cards = ""
    icons = {
        "images": "🖼️",
        "logos": "🏷️",
        "files": "📄",
        "fonts": "🔤",
        "videos": "🎬",
    }
    for name in ASSET_DIRS:
        file_list = categories.get(name, [])
        count = len(file_list)
        icon = icons.get(name, "📁")
        cards += f"""
      <a href="{name}/" class="block bg-white rounded-2xl shadow-md hover:shadow-xl transition-shadow p-6 border border-gray-100 hover:border-blue-200">
        <div class="text-4xl mb-3">{icon}</div>
        <h2 class="text-xl font-semibold text-gray-800 capitalize">{html.escape(name)}</h2>
        <p class="text-sm text-gray-500 mt-1">{count} file{"s" if count != 1 else ""}</p>
      </a>"""

    return f"""{html_head("Iliad Public CDN")}
<body class="bg-gray-50 min-h-screen">
  <div class="max-w-4xl mx-auto px-4 py-12">
    <header class="text-center mb-12">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">📦 Iliad Public CDN</h1>
      <p class="text-gray-500 text-lg">Public assets hosted via GitHub Pages</p>
      <p class="text-gray-400 text-sm mt-2">
        Use direct file URLs to reference assets in your projects
      </p>
    </header>

    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
{cards}
    </section>

    <footer class="text-center text-gray-400 text-sm border-t border-gray-200 pt-6">
      <p>Iliad Development Group &mdash; Be Heard. Be Found.</p>
      <p class="mt-1">
        <a href="https://github.com/Iliad-Interactive-Group/IliadPublicCDN" class="text-blue-400 hover:text-blue-600">
          View on GitHub
        </a>
      </p>
    </footer>
  </div>
</body>
</html>
"""


def build_directory_page(dir_name: str, files: list[str]) -> str:
    if not files:
        grid = """
      <div class="col-span-full text-center py-16 text-gray-400">
        <p class="text-5xl mb-4">📭</p>
        <p class="text-lg">No files yet</p>
        <p class="text-sm mt-2">Add files to the <code class="bg-gray-100 px-2 py-1 rounded">{dir}</code> folder and push to deploy.</p>
      </div>""".replace("{dir}", html.escape(dir_name))
    else:
        items = []
        for f in sorted(files):
            escaped = html.escape(f)
            size = get_file_size(REPO_ROOT / dir_name / f)
            if is_image(f):
                items.append(f"""
      <a href="{escaped}" class="group block bg-white rounded-xl shadow-sm hover:shadow-lg transition-all border border-gray-100 hover:border-blue-200 overflow-hidden">
        <div class="aspect-square bg-gray-50 flex items-center justify-center p-2 overflow-hidden">
          <img src="{escaped}" alt="{escaped}" class="max-h-full max-w-full object-contain group-hover:scale-105 transition-transform" loading="lazy">
        </div>
        <div class="p-3 border-t border-gray-50">
          <p class="text-sm font-medium text-gray-700 truncate" title="{escaped}">{escaped}</p>
          <p class="text-xs text-gray-400 mt-0.5">{size}</p>
        </div>
      </a>""")
            elif is_video(f):
                items.append(f"""
      <a href="{escaped}" class="group block bg-white rounded-xl shadow-sm hover:shadow-lg transition-all border border-gray-100 hover:border-blue-200 overflow-hidden">
        <div class="aspect-square bg-gray-900 flex items-center justify-center p-2 overflow-hidden">
          <video src="{escaped}" class="max-h-full max-w-full object-contain" muted preload="metadata"></video>
        </div>
        <div class="p-3 border-t border-gray-50">
          <p class="text-sm font-medium text-gray-700 truncate" title="{escaped}">{escaped}</p>
          <p class="text-xs text-gray-400 mt-0.5">🎬 {size}</p>
        </div>
      </a>""")
            else:
                ext = Path(f).suffix.upper().lstrip(".") or "FILE"
                items.append(f"""
      <a href="{escaped}" class="group block bg-white rounded-xl shadow-sm hover:shadow-lg transition-all border border-gray-100 hover:border-blue-200 overflow-hidden">
        <div class="aspect-square bg-gray-50 flex items-center justify-center">
          <div class="text-center">
            <p class="text-3xl mb-2">📄</p>
            <p class="text-xs font-mono text-gray-400">{ext}</p>
          </div>
        </div>
        <div class="p-3 border-t border-gray-50">
          <p class="text-sm font-medium text-gray-700 truncate" title="{escaped}">{escaped}</p>
          <p class="text-xs text-gray-400 mt-0.5">{size}</p>
        </div>
      </a>""")
        grid = "\n".join(items)

    return f"""{html_head(f"Iliad CDN — {dir_name}")}
<body class="bg-gray-50 min-h-screen">
  <div class="max-w-6xl mx-auto px-4 py-8">
    <nav class="mb-6">
      <a href="../" class="text-blue-500 hover:text-blue-700 text-sm">&larr; Back to CDN root</a>
    </nav>

    <header class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 capitalize">/{html.escape(dir_name)}</h1>
      <p class="text-gray-500 mt-1">{len(files)} file{"s" if len(files) != 1 else ""}</p>
    </header>

    <section class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
{grid}
    </section>

    <footer class="text-center text-gray-400 text-sm border-t border-gray-200 pt-6 mt-12">
      <p>Iliad Development Group &mdash; Be Heard. Be Found.</p>
    </footer>
  </div>
</body>
</html>
"""


def main() -> None:
    # Clean previous build
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir()

    # Collect files per category
    categories: dict[str, list[str]] = {}
    for dir_name in ASSET_DIRS:
        src = REPO_ROOT / dir_name
        if not src.is_dir():
            categories[dir_name] = []
            continue

        asset_files = [
            f.name for f in src.iterdir()
            if f.is_file() and f.name not in EXCLUDED_FILES
        ]
        categories[dir_name] = asset_files

        # Copy the directory contents to _site
        dest = SITE_DIR / dir_name
        dest.mkdir(parents=True, exist_ok=True)
        for f in src.iterdir():
            if f.is_file() and f.name not in EXCLUDED_FILES:
                shutil.copy2(f, dest / f.name)

        # Generate directory index page
        (dest / "index.html").write_text(
            build_directory_page(dir_name, asset_files), encoding="utf-8"
        )

    # Generate root landing page
    (SITE_DIR / "index.html").write_text(
        build_landing_page(categories), encoding="utf-8"
    )

    # Copy any root-level static files (like CNAME for custom domain)
    cname = REPO_ROOT / "CNAME"
    if cname.exists():
        shutil.copy2(cname, SITE_DIR / "CNAME")

    total = sum(len(v) for v in categories.values())
    print(f"✅ Built _site/ with {total} assets across {len(ASSET_DIRS)} categories")


if __name__ == "__main__":
    main()

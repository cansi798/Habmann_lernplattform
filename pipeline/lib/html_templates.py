"""HTML template helpers — pure string functions, no Jinja2."""
from __future__ import annotations
from typing import Iterable


def brand_bar(asset_prefix: str = "./") -> str:
    return (
        '<div class="brand-bar">'
        f'<a href="{asset_prefix}dashboard.html">Lernplatt · by Can Siebert</a>'
        '<a href="#" class="logout">Logout</a>'
        '</div>'
    )


def crumbs(items: Iterable[dict]) -> str:
    items = list(items)
    parts = []
    for i, it in enumerate(items):
        is_last = i == len(items) - 1
        label = it["label"]
        href = it.get("href")
        if is_last or not href:
            parts.append(f"<span>{label}</span>")
        else:
            parts.append(f'<a href="{href}">{label}</a>')
    return '<div class="crumbs">' + " › ".join(parts) + "</div>"


def page(*, title: str, body: str, asset_prefix: str = "./",
         scripts: Iterable[str] = (), require_auth: bool = True) -> str:
    auth_block = (
        f'<script src="{asset_prefix}assets/auth.js"></script>\n'
        '<script>requireAuth();</script>\n'
        if require_auth else ""
    )
    script_tags = "\n".join(f'<script src="{s}"></script>' for s in scripts)
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lernplatt · {title}</title>
  <link rel="stylesheet" href="{asset_prefix}assets/style.css">
</head>
<body>
{auth_block}{body}
<script src="{asset_prefix}assets/app.js"></script>
{script_tags}
</body>
</html>
"""

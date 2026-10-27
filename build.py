"""Build the standalone PWA (index.html) from app.html, the same page that is published as the Claude artifact.

    python3 build.py
"""
from pathlib import Path

here = Path(__file__).parent
body = (here / "app.html").read_text()
head = """<!doctype html>
<html lang="ms">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#6b0f1a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Tabung Emas">
<link rel="manifest" href="manifest.json">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
<style>[hidden]{display:none!important}img{max-width:100%}</style>
</head>
<body>
"""
sw = """<script>
if ('serviceWorker' in navigator && location.protocol.startsWith('http')) navigator.serviceWorker.register('sw.js').catch(() => {});
</script>
"""
(here / "index.html").write_text(head + body + sw + "</body>\n</html>\n")
print("index.html built")

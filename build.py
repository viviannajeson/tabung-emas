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
<meta name="apple-mobile-web-app-title" content="Tabung Emas Saya">
<link rel="manifest" href="manifest.json">
<link rel="icon" href="favicon.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="description" content="Jejak simpanan emas GAP: matlamat, bajet bulanan, rekod belian dan zakat. Bimbingan Vivianna Tora Jeson.">
<meta property="og:type" content="website">
<meta property="og:title" content="Tabung Emas Saya">
<meta property="og:description" content="Simpan · Tambah · Capai Matlamat. Bimbingan Vivianna Tora Jeson.">
<meta property="og:url" content="https://viviannajeson.github.io/tabung-emas/">
<meta property="og:image" content="https://viviannajeson.github.io/tabung-emas/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
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

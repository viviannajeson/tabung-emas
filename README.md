# Tabung Emas

Web app (PWA) untuk jejak simpanan emas GAP. Satu fail HTML, tiada server, semua data disimpan dalam telefon pengguna (localStorage).

## Fungsi

- **Utama**: jumlah gram, nilai ikut harga hari ini, untung/rugi, gram ditambah tahun ini, bilangan kali menyimpan, bulan berturut-turut, purata harga beli, progress matlamat, status simpanan bulan ini dan checklist 24 bulan (tekan bulan untuk tanda sendiri).
- **Matlamat**: set matlamat (cth. Umrah, RM 100,000 dalam 8 tahun). App kira berapa gram sebulan/setahun dan progress setiap tahun. Masukkan bajet bulanan untuk dapat anggaran tarikh capai, dan berapa gram sebulan diperlukan untuk capai dalam tempoh asal.
- **Rekod**: rekod beli dan jual/tebus (tarikh, RM, harga/g, gram dikira automatik). Status zakat emas: baki ke nisab (lalai 85g), atau anggaran zakat 2.5% bila cukup nisab.
- **Harga**: harga GAP hari ini (dimasukkan sendiri), semak harga pada mana-mana tarikh dalam sejarah, berapa untung jika simpan RM1,000 pada tarikh itu, dan graf harga.
- **Profil**: nama, nisab, kad penasihat/dealer dengan butang WhatsApp, backup/pulih data (.json), padam data.

Harga GAP tidak ada API awam, jadi harga dimasukkan sendiri. Setiap harga yang dimasukkan (dan harga pada setiap rekod belian) disimpan sebagai sejarah harga.

## Guna

Link app: https://viviannajeson.github.io/tabung-emas/

Buka `index.html` di browser, atau host repo ini (GitHub Pages) dan pilih **Add to Home Screen** supaya ia jadi macam app di telefon dan boleh guna offline.

Untuk cuba di komputer:

```
python3 -m http.server 8000
# buka http://localhost:8000
```

## Kemas kini

`app.html` ialah sumber utama (sama dengan halaman yang diterbitkan sebagai link Claude). Selepas ubah `app.html`, jalankan `python3 build.py` untuk jana semula `index.html`.

## Ikon dan thumbnail

Reka bentuk ikon ada dalam `brand/icon-art.html`. Untuk jana semula gambar: `node brand/render-icons.js $PWD/brand` (perlu Playwright), kemudian ubah saiz ke `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `apple-touch-icon.png`, `favicon.png` dan `og-image.jpg`.

## Harga automatik

`.github/workflows/update-price.yml` menjalankan `scripts/update_price.py` setiap 30 minit (8 pagi hingga 12 malam waktu Malaysia). Skrip membaca harga GAP 1 gram dari publicgold.com.my dan mengemas kini `price.json` jika harga berubah. App membaca `price.json` dari raw.githubusercontent.com (cepat) atau dari GitHub Pages.

Untuk jalankan segera: tab **Actions** → **Kemas kini harga GAP** → **Run workflow**.

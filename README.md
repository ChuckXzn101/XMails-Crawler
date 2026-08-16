# XMails-Crawler

Tools Python Berfungsi untuk scraping Gmail Dan Nomor Telepon Pada Suatu Website

## Fitur

- Scraping email dari berbagai sumber (HTML, JavaScript, CSS, komentar, meta tags)
- Scraping nomor telepon
- Scraping parameter URL
- Multi-threading untuk kecepatan maksimal
- Rotate User-Agent & Proxy anti detection
- Progress bar warna-warni
- Tidak ada delay, crawling super cepat

## Cara Install Tools

### Termux

pkg update && pkg upgrade -y
pkg install pip -y
pkg install python -y
pkg install git -y
git clone https://github.com/ChuckXzn101/XMails-Crawler.git
cd XMails-Crawler
pip install -r requirements.txt
python xmail_crawl.py -h

### Linux

sudo su
sudo apt update && sudo apt upgrade -y
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo apt install git -y
git clone https://github.com/ChuckXzn101/XMails-Crawler.git
cd XMails-Crawler
pip install -r requirements.txt
python xmail_crawl.py -h

## Cara Penggunaan

### Command Dasar

python xmail_crawl.py <url_target> -o <output_file>

### Contoh

python xmail_crawl.py https://example.com -o hasil_crawl.txt
python xmail_crawl.py https://target.com -o email_phone.txt

### Parameter

url                     Target URL yang akan di-crawl
-o, --output            Nama file output (default: hasil.txt)

## Output

Hasil crawling akan disimpan dalam file dengan format:

HASIL CRAWLING
============================================================
Target: https://example.com
Domain: example.com
Waktu: 2024-01-01 12:00:00
============================================================

TOTAL EMAIL: 10
----------------------------------------
admin@example.com
contact@example.com
info@example.com

TOTAL NOMOR TELEPON: 5
----------------------------------------
08123456789
081234567890
+6281234567890

TOTAL PARAMETER DITEMUKAN: 15
----------------------------------------
id
page
category
search

TOTAL URL DIKUNJUNGI: 50
----------------------------------------
https://example.com
https://example.com/about
https://example.com/contact

## Catatan Penting

Tools Ini Dirancang Untuk Penetration Testing (Pentest) Saja!

- Hanya gunakan pada website yang Anda miliki atau memiliki izin
- Dilarang keras menggunakan untuk aktivitas ilegal
- Script ini tidak dienkripsi, bisa kalian kembangkan lagi!
- Gunakan dengan bijak dan bertanggung jawab

## Requirements

- Python 3.6+
- requests
- beautifulsoup4
- lxml
- urllib3

## Kontributor

Creator: ChuckXzn_101
Tiktok: @chuckerrorsyntax

## Lisensi

Script ini open source dan bebas dimodifikasi untuk keperluan pembelajaran dan pengembangan.

import requests
import random
from urllib.parse import urljoin
from termcolor import colored
from fpdf import FPDF
import socket
import re
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from art import text2art
import signal
import sys

# Data jalur dan plugin yang lebih lengkap
paths = [
    "/wp-config.php", "/xmlrpc.php", "/readme.html", "/license.txt", "/robots.txt",
    "/sitemap.xml", "/.env", "/wp-content/debug.log", "/.htaccess", "/backup.zip",
    "/wp-content/uploads/", "/wp-admin/", "/wp-includes/", "/wp-content/plugins/",
    "/wp-content/themes/", "/wp-login.php", "/install.php", "/database.sql", "/backup.sql",
    "/phpinfo.php", "/error_log", "/server-status", "/cgi-bin/", "/admin.php",
    "/config.php", "/web.config", "/access.log", "/error.log", "/dump.sql",
    "/temp/", "/tmp/", "/logs/", "/log/", "/backups/", "/old/", "/index.php.bak",
    "/index.html.bak", "/.git/", "/.svn/", "/.hg/", "/.DS_Store", "/composer.json",
    "/composer.lock", "/yarn.lock", "/package.json", "/package-lock.json", "/setup.php",
    "/config.yaml", "/config.json", "/database.json", "/config.inc", "/local.xml"
]

plugins = [
    "elementor", "woocommerce", "revslider", "wpforms", "contact-form-7",
    "yoast-seo", "all-in-one-seo-pack", "classic-editor", "wp-super-cache",
    "nextgen-gallery", "duplicator", "wp-rocket", "updraftplus", "wordfence",
    "wp-fastest-cache", "loginizer", "smush", "redirection", "akismet",
    "wp-optimize", "litespeed-cache", "jetpack", "better-search-replace",
    "rank-math-seo", "seo-press", "broken-link-checker", "google-site-kit",
    "w3-total-cache", "the-events-calendar", "mainwp-child", "all-in-one-wp-migration",
    "shortcodes-ultimate", "slider-revolution", "wp-mail-smtp", "advanced-custom-fields",
    "tablepress", "duplicator-pro", "ninja-forms", "elementor-pro", "ithemes-security",
    "custom-post-type-ui", "really-simple-ssl", "hummingbird", "wp-user-avatar",
    "bbpress", "buddypress", "woocommerce-subscriptions", "social-media-share-buttons",
    "envato-elements", "wp-review", "wpdiscuz", "restrict-content-pro"
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edge/94.0.992.47",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edge/89.0.774.77",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.0.818.62",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edge/87.0.664.60",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edge/88.0.705.81",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Mozilla/5.0 (Windows NT 6.3; rv:76.0) Gecko/20100101 Firefox/76.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edge/91.0.864.64",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edge/91.0.864.59",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.3; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edge/88.0.705.88",
    "Mozilla/5.0 (Windows NT 6.1; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
    "Mozilla/5.0 (X11; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.0; rv:63.0) Gecko/20100101 Firefox/63.0",
    "Mozilla/5.0 (Windows NT 6.0; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edge/92.0.902.55",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edge/94.0.992.55",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edge/93.0.961.44",
    "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edge/87.0.664.66",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edge/89.0.774.55",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edge/85.0.564.51",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.0.818.51",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Edge/80.0.361.62",
    "Mozilla/5.0 (Windows NT 6.3; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Mozilla/5.0 (Windows NT 6.0; rv:58.0) Gecko/20100101 Firefox/58.0",
    "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edge/81.0.416.77",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Edge/80.0.361.69",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36 Edge/77.0.235.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 Edge/75.0.142.0",
    "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 Edge/73.0.309.71",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36 Edge/70.0.3538.77",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 Edge/68.0.3440.118",
    "Mozilla/5.0 (Windows NT 6.0; rv:62.0) Gecko/20100101 Firefox/62.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 Edge/68.0.3440.118",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36 Edge/60.0.3112.113",
    "Mozilla/5.0 (Windows NT 6.0; rv:56.0) Gecko/20100101 Firefox/56.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/64.0.3282.140",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36 Edge/14.14393",
]

results = {"success": [], "protected": [], "not_found": [], "errors": [], "subdomains": [], "plugins_found": [], "api_endpoints": []}

# Menangani Ctrl+C untuk menghentikan skrip dengan cara yang bersih
def handle_interrupt(signal, frame):
    print(colored("\n[!] Skrip dihentikan oleh pengguna.", "red"))
    save_results()  # Simpan hasil saat penghentian
    sys.exit(0)

# Mengatur hasil dalam JSON dengan format yang lebih keren
def save_results():
    print(colored("\n[+] Menyimpan hasil pemindaian...\n", "cyan"))
    file_name = input(colored("[?] Masukkan nama file penyimpanan PDF (biarkan kosong untuk default): ", "yellow")).strip()
    if not file_name:
        file_name = "scan_hasil.json"
    with open(file_name, "w") as outfile:
        json.dump(results, outfile, indent=4, sort_keys=True)
    print(colored(f"[+] Hasil pemindaian disimpan di {file_name}\n", "blue"))

# Membuat laporan PDF yang lebih canggih
def create_pdf_report(report_name):
    pdf = FPDF()
    pdf.add_page()

    # Header dengan logo dan desain keren
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt="Laporan Pemindaian Keamanan WordPress By RenXploit👑", ln=True, align="C")
    pdf.ln(10)

    # Menambahkan nama laporan
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Laporan Detil Pemindaian {report_name}", ln=True, align="C")
    pdf.ln(5)

    # Menambahkan kategori hasil
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, 'Kategori', border=1, align='C')
    pdf.cell(0, 10, 'URL', border=1, align='C')
    pdf.ln()

    # Memasukkan hasil dalam tabel dengan warna dan padding
    pdf.set_font("Arial", size=10)
    categories = ['success', 'protected', 'not_found', 'errors', 'subdomains']
    for category in categories:
        if results[category]:
            pdf.set_fill_color(200, 220, 255)  # Warna untuk baris kategori
            pdf.cell(40, 10, category.capitalize(), border=1, fill=True, align='C')
            for url in results[category]:
                # Cek dan pastikan URL valid dan tidak kosong
                if isinstance(url, str) and url.strip() != "":
                    pdf.cell(0, 10, url, border=1, align='C')
                else:
                    pdf.cell(0, 10, "URL tidak valid", border=1, align='C')
                pdf.ln()
            pdf.ln(2)  # Spasi antar kategori

    # Menyimpan laporan ke PDF
    pdf.output(f"{report_name}")
    print(colored(f"[+] Laporan PDF berhasil dibuat: {report_name}", "green"))

# Pemindaian subdomain
def find_subdomains(domain):
    print(colored("\n[+] Memulai pemindaian subdomain...\n", "cyan"))
      subdomains = [
        "www", "mail", "ftp", "cpanel", "webmail", "blog", "dev", "shop", "staging", "test",
        "admin", "m", "secure", "support", "portal", "shop", "app", "api", "cloud", "web", 
        "store", "test1", "beta", "help", "dev1", "img", "media", "events", "forum", "news", 
        "video", "docs", "blog1", "contact", "home", "about", "devtest", "dashboard", "stats", 
        "db", "files", "support1", "secure2", "shop1", "partners", "hr", "careers", "payment", 
        "pricing", "offers", "sign-in", "signin", "login", "register", "my", "services", 
        "vip", "pay", "members", "game", "games", "account", "profile", "jobs", "helpdesk", 
        "support2", "admin1", "business", "apps", "store1", "secure3", "testsite", "qa", 
        "intranet", "edu", "wiki", "api1", "docs1", "docs2", "media1", "assets", "cdn", "storage", 
        "backup", "review", "store2", "products", "shop2", "tickets", "tracker", "payment1", 
        "cms", "task", "orders", "subscription", "services1", "devops", "analytics", "research", 
        "recruit", "events1", "support3", "log", "update", "patch", "campaign", "beta1", 
        "test2", "feedback", "myaccount", "x", "y", "z", "v2", "v3", "staging1", "v4", "staging2",
        "release", "v5", "review1", "preprod", "audit", "secure4", "apps1", "apps2"
    ]
    for sub in subdomains:
        subdomain = f"{sub}.{domain}"
        try:
            socket.gethostbyname(subdomain)
            results["subdomains"].append(subdomain)
            print(colored(f"[+] Subdomain ditemukan: {subdomain}", "green"))
        except socket.gaierror:
            print(f"[-] Tidak ditemukan subdomain: {subdomain}")

# Menghasilkan header acak untuk permintaan HTTP
def generate_headers():
    return {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://google.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    }

# Menyiapkan sesi dengan pengaturan retry
def setup_retry_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Pemindaian URL dan status HTTP
def scan_url(url):
    headers = generate_headers()
    try:
        session = setup_retry_session()
        response = session.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            results["success"].append(url)
            print(colored(f"[+] Ditemukan: {url} (Status: 200)", "blue"))
            return colored(f"[+] Ditemukan: {url} (Status: 200)", "blue")
        elif response.status_code == 403:
            results["protected"].append(url)
            print(colored(f"[-] Terlindungi: {url} (Status: 403)", "yellow"))
            return colored(f"[-] Terlindungi: {url} (Status: 403)", "yellow")
        else:
            results["not_found"].append(url)
            print(f"[-] Tidak ditemukan: {url} (Status: {response.status_code})")
            return f"[-] Tidak ditemukan: {url} (Status: {response.status_code})"
    except requests.exceptions.RequestException as e:
        results["errors"].append({"url": url, "error": str(e)})
        print(colored(f"[-] Error saat mengakses {url}: {e}", "white"))
        return colored(f"[-] Error saat mengakses {url}: {e}", "white")

# Pemindaian plugin
def scan_plugins(target_url):
    print(colored("\n[+] Memulai pemindaian plugin...\n", "cyan"))
    for plugin in plugins:
        url = urljoin(target_url, f"/wp-content/plugins/{plugin}/")
        print(scan_url(url))

# Pemindaian jalur plugin dan API
def scan_api_endpoints(target_url):
    print(colored("\n[+] Memulai pemindaian API WordPress...\n", "cyan"))
    api_endpoints = [
    "/wp-json/wp/v2/users/",
    "/wp-json/wp/v2/posts/",
    "/wp-json/wp/v2/pages/",
    "/wp-json/wp/v2/comments/",
    "/wp-json/oembed/1.0/embed",
    "/wp-json/wp/v2/media/",
    "/wp-json/wp/v2/categories/",
    "/wp-json/wp/v2/tags/",
    "/wp-json/wp/v2/settings/",
    "/wp-json/wp/v2/themes/",
    "/wp-json/wp/v2/plugins/",
    "/wp-json/wp/v2/blocks/",
    "/wp-json/wp/v2/block-renderer/",
    "/wp-json/wp/v2/types/",
    "/wp-json/wp/v2/statuses/",
    "/wp-json/wp/v2/search/",
    "/wp-json/wp/v2/taxonomies/",
    "/wp-json/wp/v2/menu-locations/",
    "/wp-json/wp/v2/menu-items/",
    "/wp-json/wp/v2/navigation/",
    "/wp-json/wp/v2/templates/",
    "/wp-json/wp/v2/template-parts/",
    "/wp-json/wp/v2/sidebar/",
    "/wp-json/wp/v2/widgets/",
    "/wp-json/wp/v2/themes/active",
    "/wp-json/wp/v2/posts/{id}/revisions",
    "/wp-json/wp/v2/posts/{id}/autosaves",
    "/wp-json/wp/v2/posts/{id}/lock",
    "/wp-json/wp/v2/posts/{id}/unlock",
    "/wp-json/wp/v2/posts/{id}/lock-check",
    "/wp-json/wp/v2/posts/{id}/revisions/{revision_id}",
    "/wp-json/wp/v2/media/{id}",
    "/wp-json/wp/v2/media/{id}/edit",
    "/wp-json/wp/v2/media/{id}/delete",
    "/wp-json/wp/v2/settings/general",
    "/wp-json/wp/v2/settings/reading",
    "/wp-json/wp/v2/settings/discussion",
    "/wp-json/wp/v2/settings/media",
    "/wp-json/wp/v2/users/me",
    "/wp-json/wp/v2/users/me/preferences",
    "/wp-json/wp/v2/comments/{id}",
    "/wp-json/wp/v2/comments/{id}/edit",
    "/wp-json/wp/v2/comments/{id}/reply",
    "/wp-json/wp/v2/plugins/active",
    "/wp-json/wp/v2/plugins/inactive",
    "/wp-json/wp/v2/plugins/install",
    "/wp-json/wp/v2/plugins/delete",
    "/wp-json/wp/v2/plugins/{plugin_id}",
    "/wp-json/wp/v2/themes/{theme_id}"
    ]
    for api in api_endpoints:
        url = urljoin(target_url, api)
        print(scan_url(url))

# Pemindaian keseluruhan dan merangkum hasil
def summarize_results():
    print(colored("\n[+] Ringkasan Hasil Pemindaian:\n", "magenta"))
    for key, value in results.items():
        print(colored(f"{key.upper()}: {len(value)} ditemukan", "yellow"))

# Fungsi utama untuk menjalankan pemindaian
def main():
    signal.signal(signal.SIGINT, handle_interrupt)  # Menangkap Ctrl+C
    print(colored(text2art("WP Scanner", font="block"), "cyan"))
    target_url = input(colored("[?] Masukkan URL target (contoh: https://example.com): ", "yellow")).strip()
    domain = re.sub(r"https?://(www\.)?", "", target_url).split("/")[0]
    find_subdomains(domain)

    print(colored("\n[+] Memulai pemindaian jalur sensitif...\n", "cyan"))
    for path in paths:
        url = urljoin(target_url, path)
        print(scan_url(url))

    scan_plugins(target_url)
    scan_api_endpoints(target_url)
    summarize_results()

    # Input untuk nama laporan PDF
    report_name = input(colored("[?] Masukkan nama untuk laporan PDF (biarkan kosong untuk default): ", "yellow")).strip()
    if not report_name:
        report_name = "scan_hasil"
    create_pdf_report(report_name)

    # Simpan hasil pemindaian ke file JSON
    save_results()

if __name__ == "__main__":
    main()

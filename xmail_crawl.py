#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CARA PENGGUNAAN:
python xmail_crawl.py <url_target> -o <output_file>

CONTOH:
python xmail_crawl.py https://example.com -o hasil.txt
"""

import re
import sys
import time
import random
import requests
import argparse
import hashlib
import json
import threading
from urllib.parse import urlparse, urljoin, urlencode, parse_qs, quote
from datetime import datetime
from bs4 import BeautifulSoup, Comment
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

BANNER = f"""
{RED}.__    ._____                   ___.                    __                                
|__| __| _/  | __   ____ ___.__.\_ |__   ___________  _/  |_  ____ _____    _____   ______
|  |/ __ ||  |/ / _/ ___<   |  | | __ \\_/ __ \\_  __ \\ \\   __\\/ __ \\\\__  \\  /     \\ /  ___/
|  / /_/ ||    <  \\  \\___\\___  | | \\_\\ \\  ___/|  | \\/  |  | \\  ___/ / __ \\|  Y Y  \\\\___ \\ 
|__\\____ ||__|_ \\  \\___  > ____| |___  /\\___  >__|     |__|  \\___  >____  /__|_|  /____  >
        \\/     \\/      \\/\\/          \\/     \\/                   \\/     \\/      \\/     \\/ {RESET}
"""

def fetch_proxies():
    proxies = []
    urls = [
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt',
        'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
        'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
    ]
    for url in urls:
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                for line in resp.text.splitlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if ':' in line:
                            proxies.append(f'http://{line}')
                            proxies.append(f'https://{line}')
        except:
            continue
    return list(set(proxies))[:100]

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)',
]

PAYLOADS = [
    'id', 'page', 'cat', 'category', 'post', 'article', 'news', 'blog', 'p',
    'product', 'prod', 'item', 'detail', 'view', 'show', 'read', 'pid',
    'action', 'do', 'act', 'cmd', 'command', 'exec', 'run', 'execute',
    'q', 'query', 's', 'search', 'keyword', 'terms', 'find', 'lookup',
    'name', 'nama', 'title', 'judul', 'slug', 'permalink', 'alias',
    'type', 'sort', 'order', 'by', 'limit', 'offset', 'start', 'end',
    'page_id', 'post_id', 'user_id', 'member_id', 'cat_id', 'blog_id',
    'tag', 'tags', 'filter', 'filterby', 'group', 'groupby', 'orderby',
    'date', 'month', 'year', 'day', 'time', 'hour', 'minute', 'second',
    'debug', 'test', 'mode', 'format', 'output', 'callback', 'jsonp',
    'lang', 'language', 'locale', 'country', 'region', 'city', 'state',
    'key', 'api_key', 'apikey', 'token', 'auth', 'hash', 'signature',
    'url', 'redirect', 'return', 'goto', 'next', 'prev', 'back',
    'file', 'path', 'dir', 'folder', 'filename', 'ext', 'extension',
    'download', 'upload', 'import', 'export', 'backup', 'restore',
    'config', 'conf', 'setting', 'option', 'pref', 'preference',
    'user', 'username', 'login', 'email', 'mail', 'phone', 'mobile',
    'password', 'pass', 'pwd', 'secret', 'private', 'token', 'pin',
    'admin', 'root', 'super', 'master', 'guest', 'anonymous',
    'view', 'display', 'render', 'template', 'theme', 'skin',
    'src', 'source', 'data', 'info', 'detail', 'description',
    'uid', 'uuid', 'guid', 'sid', 'session', 'token', 'csrf',
    'ref', 'referer', 'source', 'utm_source', 'utm_medium', 'utm_campaign',
    'gclid', 'fbclid', 'msclkid', 'refid', 'clickid', 'campaign',
    'from', 'to', 'cc', 'bcc', 'subject', 'body', 'message', 'content',
    'nama_depan', 'nama_belakang', 'nama_lengkap', 'fullname', 'firstname', 'lastname',
    'alamat', 'address', 'kota', 'provinsi', 'kode_pos', 'zipcode', 'poscode',
    'telepon', 'handphone', 'hp', 'whatsapp', 'wa', 'line', 'telegram',
    'instagram', 'twitter', 'facebook', 'youtube', 'tiktok', 'linkedin',
    'website', 'url', 'link', 'domain', 'subdomain',
    'server', 'host', 'port', 'ip', 'hostname', 'server_name',
    'db', 'database', 'dbname', 'host', 'port', 'username', 'password',
    'table', 'tables', 'column', 'columns', 'field', 'fields',
    'where', 'and', 'or', 'not', 'in', 'like', 'between',
    'order', 'group', 'having', 'limit', 'offset', 'join',
    'select', 'insert', 'update', 'delete', 'drop', 'create', 'alter',
    'head', 'header', 'footer', 'sidebar', 'content', 'main',
    'login', 'logout', 'signup', 'register', 'forgot', 'reset', 'change',
    'activate', 'verify', 'confirm', 'validate', 'authenticate',
    'cookie', 'session', 'cache', 'redis', 'memcache',
    'mail', 'smtp', 'pop3', 'imap', 'sendmail', 'postfix',
    'ftp', 'sftp', 'ssh', 'telnet', 'rdp', 'vnc',
    'proxy', 'proxy_list', 'proxy_ip', 'proxy_port',
    'get', 'post', 'put', 'delete', 'patch', 'options', 'head',
    'json', 'xml', 'html', 'plain', 'raw', 'binary',
]

class MailCrawler:
    def __init__(self, target, output=None):
        self.target = target.rstrip('/')
        self.domain = urlparse(target).netloc
        self.output = output or f"crawl_{self.domain}.txt"
        self.visited = set()
        self.emails = set()
        self.phones = set()
        self.urls_found = set()
        self.params_found = set()
        self.proxies = fetch_proxies()
        self.total_requests = 0
        self.running = True
        self.queue = []
        self.queue_index = 0
        self.lock = threading.Lock()
        self.progress = 0
        
        self.all_paths = [
            '/', '/index.html', '/index.php', '/index.asp', '/index.aspx',
            '/contact', '/contact-us', '/contact.php', '/contact.html', '/contact.asp',
            '/about', '/about-us', '/about.php', '/about.html',
            '/team', '/our-team', '/staff', '/people', '/member', '/members',
            '/career', '/careers', '/jobs', '/recruitment', '/employment', '/kerja',
            '/hr', '/human-resources', '/employee', '/employees', '/karyawan',
            '/support', '/help', '/helpdesk', '/faq', '/support.php',
            '/sales', '/marketing', '/business', '/partnership', '/bisnis',
            '/partner', '/partners', '/vendor', '/vendors', '/supplier',
            '/customer', '/customers', '/client', '/clients', '/pelanggan',
            '/service', '/services', '/product', '/products', '/produk',
            '/blog', '/news', '/article', '/articles', '/berita',
            '/author', '/authors', '/contributor', '/contributors',
            '/profile', '/profiles', '/account', '/accounts', '/akun',
            '/login', '/register', '/signup', '/subscribe', '/daftar',
            '/newsletter', '/mailing-list', '/email', '/email.php', '/mail',
            '/webmail', '/inbox', '/send', '/mail.php',
            '/admin', '/administrator', '/webmaster',
            '/info', '/information', '/company', '/corporate', '/perusahaan',
            '/page', '/pages', '/post', '/posts',
            '/tag', '/tags', '/category', '/categories', '/kategori',
            '/search', '/sitemap', '/sitemap.xml', '/sitemap.php',
            '/robots.txt', '/.env', '/config', '/config.php', '/configuration',
            '/backup', '/backups', '/temp', '/tmp',
            '/test', '/tests', '/demo', '/sample',
            '/api', '/v1', '/v2', '/v3', '/rest', '/graphql',
            '/docs', '/documentation', '/manual', '/guide', '/tutorial',
            '/forum', '/community', '/chat', '/discuss',
            '/wp-admin', '/wp-login', '/wp-json', '/wp-content', '/wp-includes',
            '/administrator', '/backend', '/dashboard', '/panel', '/cpanel',
            '/phpmyadmin', '/mysql', '/database', '/db', '/sql',
            '/logs', '/error', '/errors', '/debug',
            '/upload', '/uploads', '/files', '/download', '/downloads',
            '/gallery', '/images', '/img', '/photo', '/photos', '/foto',
            '/video', '/videos', '/audio', '/music',
            '/shop', '/store', '/cart', '/checkout', '/belanja',
            '/event', '/events', '/seminar', '/workshop', '/pelatihan',
            '/pricing', '/price', '/harga', '/paket', '/package',
            '/testimonial', '/testimonials', '/review', '/reviews',
            '/portfolio', '/portofolio', '/project', '/projects',
            '/layanan', '/produk', '/faq', '/tanya', '/pertanyaan',
            '/privacy', '/policy', '/terms', '/syarat', '/ketentuan',
            '/disclaimer', '/copyright', '/hakcipta',
            '/sitemap_index.xml', '/post-sitemap.xml', '/page-sitemap.xml',
            '/feed', '/rss', '/atom', '/xmlrpc.php',
            '/.well-known', '/.git', '/.svn', '/.htaccess', '/.htpasswd',
            'backup.zip', 'backup.tar', 'backup.gz', 'dump.sql',
            'database.sql', 'db.sql', 'data.sql',
            'config.ini', 'settings.ini', 'config.yml', 'settings.yml',
            'conf.php', 'config.php', 'settings.php', 'db.php', 'connect.php',
            'index.php', 'main.php', 'home.php', 'default.php',
            'login.php', 'register.php', 'signup.php', 'admin.php',
            'contact.php', 'about.php', 'team.php', 'careers.php',
        ]
        
        for path in self.all_paths:
            self.queue.append(urljoin(self.target, path))
        self.queue.append(self.target)
        
        for param in PAYLOADS:
            for value in ['1', '0', 'true', 'false', 'test', 'admin', 'user', '123', 'id']:
                self.queue.append(f"{self.target}?{param}={value}")
                self.queue.append(f"{self.target}/?{param}={value}")
                self.queue.append(f"{self.target}?{param}={value}&page=1")
                self.queue.append(f"{self.target}?{param}={value}&limit=10")
                self.queue.append(f"{self.target}?{param}={value}&sort=asc")
                self.queue.append(f"{self.target}?{param}={value}&order=id")
        
    def get_headers(self):
        return {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': self.target,
            'DNT': '1'
        }
    
    def get_proxy(self):
        if self.proxies:
            return {'http': random.choice(self.proxies), 'https': random.choice(self.proxies)}
        return None
    
    def extract_data(self, text, url):
        if not text:
            return
        
        email_patterns = [
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            r'[a-zA-Z0-9._%+-]+\s*\[\s*at\s*\]\s*[a-zA-Z0-9.-]+\s*\.\s*[a-zA-Z]{2,}',
            r'[a-zA-Z0-9._%+-]+\s*\(\s*at\s*\)\s*[a-zA-Z0-9.-]+\s*\.\s*[a-zA-Z]{2,}',
            r'[a-zA-Z0-9._%+-]+\s*@\s*[a-zA-Z0-9.-]+\s*\.\s*[a-zA-Z]{2,}',
            r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            r'([a-zA-Z0-9._%+-]+)\s+at\s+([a-zA-Z0-9.-]+)\s+dot\s+([a-zA-Z]{2,})',
            r'([a-zA-Z0-9._%+-]+)\s+\[at\]\s+([a-zA-Z0-9.-]+)\s+\[dot\]\s+([a-zA-Z]{2,})',
            r'([a-zA-Z0-9._%+-]+)\s+\(at\)\s+([a-zA-Z0-9.-]+)\s+\(dot\)\s+([a-zA-Z]{2,})',
            r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})',
            r'([a-zA-Z0-9._%+-]+)\.([a-zA-Z0-9.-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})',
        ]
        
        for pattern in email_patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            for match in found:
                if isinstance(match, tuple):
                    if len(match) == 3:
                        email = f"{match[0]}@{match[1]}.{match[2]}"
                    elif len(match) == 4:
                        email = f"{match[0]}.{match[1]}@{match[2]}.{match[3]}"
                    else:
                        continue
                else:
                    email = match
                
                email = email.replace('[at]', '@').replace('(at)', '@')
                email = email.replace('[ at ]', '@').replace('( at )', '@')
                email = email.replace(' at ', '@').replace(' dot ', '.')
                email = email.replace('[dot]', '.').replace('(dot)', '.')
                email = email.replace('[ dot ]', '.').replace('( dot )', '.')
                email = re.sub(r'\s+', '', email.strip())
                email = email.replace('@', '@')  
                
                if '@' in email and '.' in email and len(email) > 5 and len(email) < 100:
                    if email not in self.emails:
                        self.emails.add(email)
                        print(f"{GREEN}[EMAIL] {email}{RESET}")
        
        phone_patterns = [
            r'\+?62[-\s]?[0-9]{9,13}',
            r'08[0-9]{8,11}',
            r'08[0-9]{2}[-\s]?[0-9]{3,4}[-\s]?[0-9]{3,4}',
            r'0[0-9]{9,12}',
            r'\+?[0-9]{1,3}[-\s]?[0-9]{2,4}[-\s]?[0-9]{3,5}[-\s]?[0-9]{3,5}',
            r'\(\+?[0-9]{1,3}\)[-\s]?[0-9]{2,4}[-\s]?[0-9]{3,5}[-\s]?[0-9]{3,5}',
            r'tel:([0-9+\-\s()]+)',
            r'phone:([0-9+\-\s()]+)',
            r'whatsapp:([0-9+\-\s()]+)',
            r'wa:([0-9+\-\s()]+)',
            r'telepon:([0-9+\-\s()]+)',
            r'handphone:([0-9+\-\s()]+)',
            r'hp:([0-9+\-\s()]+)',
            r'[0-9]{3,4}[-\s]?[0-9]{3,4}[-\s]?[0-9]{3,4}',
        ]
        
        for pattern in phone_patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            for phone in found:
                if isinstance(phone, tuple):
                    phone = phone[0] if phone else ''
                phone = re.sub(r'[^0-9+]', '', str(phone).strip())
                if len(phone) >= 8 and len(phone) <= 15:
                    if phone not in self.phones:
                        self.phones.add(phone)
                        print(f"{BLUE}[PHONE] {phone}{RESET}")
    
    def crawl_page(self, url):
        if url in self.visited:
            return
        
        with self.lock:
            self.visited.add(url)
            self.total_requests += 1
        
        try:
            headers = self.get_headers()
            proxy = self.get_proxy()
            
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10, verify=False)
            
            if response.status_code == 200:
                parsed = urlparse(url)
                if parsed.query:
                    params = parse_qs(parsed.query)
                    for key in params.keys():
                        with self.lock:
                            if key not in self.params_found:
                                self.params_found.add(key)
                                print(f"{YELLOW}[PARAM] {key}{RESET}")
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                self.extract_data(soup.get_text(), url)
                self.extract_data(response.text, url)
                
                for tag in soup.find_all():
                    if tag.string:
                        self.extract_data(str(tag.string), url)
                    for attr in ['href', 'src', 'title', 'alt', 'content', 'data', 'value', 'name', 'id', 'class', 'style']:
                        if tag.get(attr):
                            self.extract_data(str(tag.get(attr)), url)
                
                for script in soup.find_all('script'):
                    if script.string:
                        self.extract_data(str(script.string), url)
                    if script.get('src'):
                        src_url = urljoin(url, script.get('src'))
                        try:
                            js_resp = requests.get(src_url, headers=headers, proxies=proxy, timeout=10, verify=False)
                            if js_resp.status_code == 200:
                                self.extract_data(js_resp.text, src_url)
                        except:
                            pass
                
                for style in soup.find_all('style'):
                    if style.string:
                        self.extract_data(str(style.string), url)
                
                for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                    self.extract_data(str(comment), url)
                
                for meta in soup.find_all('meta'):
                    for attr in ['content', 'name', 'property', 'itemprop']:
                        if meta.get(attr):
                            self.extract_data(str(meta.get(attr)), url)
                
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if 'mailto:' in href:
                        self.extract_data(href, url)
                    if 'tel:' in href:
                        self.extract_data(href, url)
                    
                    full_url = urljoin(url, href)
                    if full_url.startswith(self.target) and full_url not in self.visited:
                        if not full_url.endswith(('.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.pdf', '.zip', '.tar', '.gz')):
                            self.queue.append(full_url)
                
                for img in soup.find_all('img'):
                    if img.get('alt'):
                        self.extract_data(str(img.get('alt')), url)
                    if img.get('title'):
                        self.extract_data(str(img.get('title')), url)
                    if img.get('src'):
                        self.extract_data(str(img.get('src')), url)
                
                for form in soup.find_all('form'):
                    action = form.get('action', '')
                    method = form.get('method', 'get').lower()
                    inputs = form.find_all('input')
                    for inp in inputs:
                        name = inp.get('name')
                        if name:
                            with self.lock:
                                if name not in self.params_found:
                                    self.params_found.add(name)
                                    print(f"{YELLOW}[PARAM] {name}{RESET}")
        
        except Exception as e:
            pass
    
    def worker(self):
        while self.running:
            with self.lock:
                if self.queue_index >= len(self.queue):
                    break
                url = self.queue[self.queue_index]
                self.queue_index += 1
            
            self.crawl_page(url)
            
            total = len(self.queue)
            if total > 0:
                self.progress = int((self.queue_index / total) * 100)
                if self.progress > 100:
                    self.progress = 100
    
    def animate_loading(self):
        colors = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]
        bar_length = 40
        i = 0
        
        while self.running:
            color = colors[i % len(colors)]
            percent = self.progress
            
            if percent == 0:
                bar = '░' * bar_length
            else:
                filled = int(bar_length * percent / 100)
                empty = bar_length - filled
                bar = '█' * filled + '░' * empty
            
            sys.stdout.write(f'\r{color}[{bar}] {percent:3d}% | URL: {len(self.visited):4d} | Email: {len(self.emails):3d} | Phone: {len(self.phones):3d} | Param: {len(self.params_found):3d}{RESET}')
            sys.stdout.flush()
            
            i += 1
            time.sleep(0.02)
    
    def start(self):
        print(BANNER)
        print(f"{CYAN}[*] Target: {self.target}{RESET}")
        print(f"{CYAN}[*] Domain: {self.domain}{RESET}")
        print(f"{CYAN}[*] Output: {self.output}{RESET}")
        print(f"{CYAN}[*] Proxy Loaded: {len(self.proxies)}{RESET}")
        print(f"{CYAN}[*] Total Paths: {len(self.all_paths)}{RESET}")
        print(f"{CYAN}[*] Total Queue: {len(self.queue)}{RESET}")
        print(f"{GREEN}[*] Memulai crawling...\n{RESET}")
        
        anim_thread = threading.Thread(target=self.animate_loading)
        anim_thread.daemon = True
        anim_thread.start()
        
        self.worker()
        
        self.running = False
        anim_thread.join(timeout=0.5)
        
        bar = '█' * 40
        print(f"\r{GREEN}[{bar}] 100% | URL: {len(self.visited):4d} | Email: {len(self.emails):3d} | Phone: {len(self.phones):3d} | Param: {len(self.params_found):3d}{RESET}")
        print("\n")
        self.save_results()
        self.show_summary()
    
    def save_results(self):
        with open(self.output, 'w') as f:
            f.write("="*60 + "\n")
            f.write(f"HASIL CRAWLING\n")
            f.write(f"Target: {self.target}\n")
            f.write(f"Domain: {self.domain}\n")
            f.write(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"TOTAL EMAIL: {len(self.emails)}\n")
            f.write("-"*40 + "\n")
            for email in sorted(self.emails):
                f.write(f"{email}\n")
            
            f.write(f"\n\nTOTAL NOMOR TELEPON: {len(self.phones)}\n")
            f.write("-"*40 + "\n")
            for phone in sorted(self.phones):
                f.write(f"{phone}\n")
            
            f.write(f"\n\nTOTAL PARAMETER DITEMUKAN: {len(self.params_found)}\n")
            f.write("-"*40 + "\n")
            for param in sorted(self.params_found):
                f.write(f"{param}\n")
            
            f.write(f"\n\nTOTAL URL DIKUNJUNGI: {len(self.visited)}\n")
            f.write("-"*40 + "\n")
            for url in sorted(self.visited):
                f.write(f"{url}\n")
    
    def show_summary(self):
        print("="*60)
        print(f"{GREEN}[+] TOTAL EMAIL DITEMUKAN: {len(self.emails)}{RESET}")
        print(f"{GREEN}[+] TOTAL NOMOR TELEPON: {len(self.phones)}{RESET}")
        print(f"{GREEN}[+] TOTAL PARAMETER DITEMUKAN: {len(self.params_found)}{RESET}")
        print(f"{GREEN}[+] TOTAL URL DIKUNJUNGI: {len(self.visited)}{RESET}")
        print(f"{GREEN}[+] TOTAL REQUEST: {self.total_requests}{RESET}")
        print(f"{GREEN}[+] Hasil disimpan di: {self.output}{RESET}")
        print("="*60)

def main():
    parser = argparse.ArgumentParser(description='XMail Crawl - Email, Phone & Parameter Crawler')
    parser.add_argument('url', help='Target URL')
    parser.add_argument('-o', '--output', help='File output', default='hasil.txt')
    
    args = parser.parse_args()
    
    crawler = MailCrawler(args.url, args.output)
    crawler.start()

if __name__ == '__main__':
    main()

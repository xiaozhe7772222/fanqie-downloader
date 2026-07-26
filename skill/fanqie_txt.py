#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@小哲 番茄小说下载器 - Skill 完整版
适用于 Operit AI Agent / 自动化平台
依赖: requests, beautifulsoup4, tqdm, gmssl
支持: 搜索、下载、查详情、榜单浏览、批量下载、追更检测
"""
import requests as req
from bs4 import BeautifulSoup
from tqdm import tqdm
import json, time, random, os, sys, re
CODE = [[58344, 58715], [58345, 58716]]
charset = json.loads('[["D","在","主","特","家","军","然","表","场","4","要","只","v","和","?","6","别","还","g","现","儿","岁","?","?","此","象","月","3","出","战","工","相","o","男","直","失","世","F","都","平","文","什","V","O","将","真","T","那","当","?","会","立","些","u","是","十","张","学","气","大","爱","两","命","全","后","东","性","通","被","1","它","乐","接","而","感","车","山","公","了","常","以","何","可","话","先","p","i","叫","轻","M","士","w","着","变","尔","快","l","个","说","少","色","里","安","花","远","7","难","师","放","t","报","认","面","道","S","?","克","地","度","I","好","机","U","民","写","把","万","同","水","新","没","书","电","吃","像","斯","5","为","y","白","几","日","教","看","但","第","加","候","作","上","拉","住","有","法","r","事","应","位","利","你","声","身","国","问","马","女","他","Y","比","父","x","A","H","N","s","X","边","美","对","所","金","活","回","意","到","z","从","j","知","又","内","因","点","Q","三","定","8","R","b","正","或","夫","向","德","听","更","?","得","告","并","本","q","过","记","L","让","打","f","人","就","者","去","原","满","体","做","经","K","走","如","孩","c","G","给","使","物","?","最","笑","部","?","员","等","受","k","行","一","条","果","动","光","门","头","见","往","自","解","成","处","天","能","于","名","其","发","总","母","的","死","手","入","路","进","心","来","h","时","力","多","开","已","许","d","至","由","很","界","n","小","与","Z","想","代","么","分","生","口","再","妈","望","次","西","风","种","带","J","?","实","情","才","这","?","E","我","神","格","长","觉","间","年","眼","无","不","亲","关","结","0","友","信","下","却","重","己","老","2","音","字","m","呢","明","之","前","高","P","B","目","太","e","9","起","稜","她","也","W","用","方","子","英","每","理","便","四","数","期","中","C","外","样","a","海","们","任"],["s","?","作","口","在","他","能","并","B","士","4","U","克","才","正","们","字","声","高","全","尔","活","者","动","其","主","报","多","望","放","h","w","次","年","?","中","3","特","于","十","入","要","男","同","G","面","分","方","K","什","再","教","本","己","结","1","等","世","N","?","说","g","u","期","Z","外","美","M","行","给","9","文","将","两","许","张","友","0","英","应","向","像","此","白","安","少","何","打","气","常","定","间","花","见","孩","它","直","风","数","使","道","第","水","已","女","山","解","d","P","的","通","关","性","叫","儿","L","妈","问","回","神","来","S","","四","望","前","国","些","O","v","l","A","心","平","自","无","军","光","代","是","好","却","c","得","种","就","意","先","立","z","子","过","Y","j","表","","么","所","接","了","名","金","受","J","满","眼","没","部","那","m","每","车","度","可","R","斯","经","现","门","明","V","如","走","命","y","6","E","战","很","上","f","月","西","7","长","夫","想","话","变","海","机","x","到","W","一","成","生","信","笑","但","父","开","内","东","马","日","小","而","后","带","以","三","几","为","认","X","死","员","目","位","之","学","远","人","音","呢","我","q","乐","象","重","对","个","被","别","F","也","书","稜","D","写","还","因","家","发","时","i","或","住","德","当","o","l","比","觉","然","吃","去","公","a","老","亲","情","体","太","b","万","C","电","理","?","失","力","更","拉","物","着","原","她","工","实","色","感","记","看","出","相","路","大","你","候","2","和","?","与","p","样","新","只","便","最","不","进","T","r","做","格","母","总","爱","身","师","轻","知","往","加","从","?","天","e","H","?","听","场","由","快","边","让","把","任","8","条","头","事","至","起","点","真","手","这","难","都","界","用","法","n","处","下","又","Q","告","地","5","k","t","岁","有","会","果","利","民"]]')
class Config:
    def __init__(self):
        if getattr(sys, 'frozen', False): self.script_dir = os.path.dirname(sys.executable)
        else: self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.script_dir, 'data')
        self.bookstore_dir = os.path.join(self.data_dir, 'bookstore')
        self.config_path = os.path.join(self.data_dir, 'config.json')
        self.default_config = {'kg': 2, 'kgf': '\u3000', 'delay': [50, 150], 'save_path': '', 'save_mode': 1, 'xc': 1, 'enable_chapter_numbering': False, 'max_retries': 3, 'timeout': 10, 'version': '3.0.0-skill'}
        if not os.path.exists(self.data_dir): self.config = self.default_config.copy(); self._detect_save_path()
        else: self.config = self.load_config(); 
        if not self.config.get('save_path'): self._detect_save_path()
    def _detect_save_path(self):
        candidates = ['/storage/emulated/0/番茄小说下载/', '/sdcard/番茄小说下载/', '/storage/self/primary/番茄小说下载/', os.path.join(self.script_dir, 'downloads')]
        for p in candidates:
            try: os.makedirs(p, exist_ok=True); test_file = os.path.join(p, '.write_test'); open(test_file, 'w').close(); os.remove(test_file); self.config['save_path'] = p; self.save_config(); print(f'📁 保存路径已自动设为: {p}'); return
            except: continue
        fallback = os.path.join(self.script_dir, 'downloads'); os.makedirs(fallback, exist_ok=True); self.config['save_path'] = fallback; self.save_config(); print(f'📁 保存路径已自动设为: {fallback}')
    def select_save_path(self):
        print('\n' + '=' * 50); print('  📂 选择保存路径'); print('=' * 50); print(f'  当前路径: {self.config.get("save_path", "未设置")}'); print(); print('  1. 使用默认路径 (/storage/emulated/0/番茄小说下载/)'); print('  2. 手动输入路径'); print('  3. 使用脚本目录下的 downloads 文件夹'); print('  b. 返回'); print()
        choice = input('  请选择 (1/2/3/b): ').strip()
        if choice == '1': p = '/storage/emulated/0/番茄小说下载/'
        elif choice == '2': p = input('  请输入保存路径: ').strip()
        elif choice == '3': p = os.path.join(self.script_dir, 'downloads')
        else: print('  已取消'); return
        if p:
            try: os.makedirs(p, exist_ok=True); open(os.path.join(p, '.write_test'), 'w').close(); os.remove(os.path.join(p, '.write_test')); self.config['save_path'] = p; self.save_config(); print(f'  ✅ 已设置为: {p}')
            except: print('  ❌ 路径不可写')
    def create_directories(self):
        for d in [self.data_dir, self.bookstore_dir]:
            if not os.path.exists(d): os.makedirs(d)
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w', encoding='UTF-8') as f: json.dump(self.default_config, f, indent=2, ensure_ascii=False)
        record_path = os.path.join(self.data_dir, 'record.json')
        if not os.path.exists(record_path):
            with open(record_path, 'w', encoding='UTF-8') as f: json.dump([], f)
    def __getitem__(self, key):
        try: return self.config[key]
        except: return self.default_config.get(key)
    def __setitem__(self, key, value): self.config[key] = value; self.save_config()
    def load_config(self):
        if not os.path.exists(self.data_dir): return self.default_config.copy()
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='UTF-8') as f:
                try: merged = self.default_config.copy(); merged.update(json.load(f)); return merged
                except: return self.default_config.copy()
        return self.default_config.copy()
    def save_config(self):
        if os.path.exists(self.data_dir):
            with open(self.config_path, 'w', encoding='UTF-8') as f: json.dump(self.config, f, indent=2, ensure_ascii=False)
    def get(self, key, default=None): return self.config.get(key, default)
    def set(self, key, value): self.config[key] = value; self.save_config()
config = Config(); config.create_directories()
script_dir = config.script_dir; data_dir = config.data_dir; bookstore_dir = config.bookstore_dir; record_path = os.path.join(data_dir, 'record.json')
headers_lib = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47']
session = req.Session(); session.mount('http://', req.adapters.HTTPAdapter(max_retries=3)); session.mount('https://', req.adapters.HTTPAdapter(max_retries=3))
session.headers.update({'User-Agent': random.choice(headers_lib), 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Connection': 'keep-alive'})
def interpreter(uni, mode):
    bias = uni - CODE[mode][0]
    if bias < 0 or bias >= len(charset[mode]) or charset[mode][bias] == '?': return chr(uni)
    return charset[mode][bias]
def str_interpreter(n, mode):
    s = ''
    for ch in n:
        uni = ord(ch)
        if CODE[mode][0] <= uni <= CODE[mode][1]: s += interpreter(uni, mode)
        else: s += ch
    return s
def down_zj(it):
    url = 'https://fanqienovel.com/page/' + str(it)
    response = session.get(url, timeout=config.get('timeout', 10))
    if response.status_code != 200: return ['err', {}, []]
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.find('h1')
    if not h1: return ['err', {}, []]
    name = h1.get_text(strip=True)
    chapters = {}
    chapter_divs = soup.find_all('div', class_='chapter')
    for cdiv in chapter_divs:
        for a in cdiv.find_all('a'):
            title = a.get_text(strip=True); href = a.get('href', ''); cid = href.split('/')[-1]
            if title and cid: chapters[title] = cid
    status_text = ''
    status_span = soup.find('span', class_='info-label-yellow')
    if status_span: status_text = status_span.get_text(strip=True)
    return [name, chapters, [status_text]]
def down_text(it):
    max_retries = config.get('max_retries', 3)
    for retry in range(max_retries):
        try:
            response = session.get(f"https://fanqienovel.com/reader/{it}", timeout=config.get('timeout', 10))
            if response.status_code == 200:
                text = response.text; start_marker = 'window.__INITIAL_STATE__='; start_idx = text.find(start_marker)
                if start_idx != -1:
                    start_idx += len(start_marker); depth = 0; in_string = False; escape = False; end_idx = start_idx
                    for i in range(start_idx, len(text)):
                        c = text[i]
                        if escape: escape = False; continue
                        if c == '\\': escape = True; continue
                        if c == '"': in_string = not in_string; continue
                        if in_string: continue
                        if c == '{': depth += 1
                        elif c == '}': depth -= 1
                        if depth == 0: end_idx = i + 1; break
                    raw_json = text[start_idx:end_idx]; state = json.loads(raw_json)
                    content = state.get('reader', {}).get('chapterData', {}).get('content', '')
                    if content:
                        content = str_interpreter(content, 0)
                        content = re.sub(r'<header>.*?</header>', '', content, flags=re.DOTALL)
                        content = re.sub(r'<footer>.*?</footer>', '', content, flags=re.DOTALL)
                        content = re.sub(r'</?article>', '', content)
                        content = re.sub(r'<p idx="\d+">', '\n', content); content = re.sub(r'</p>', '\n', content)
                        content = re.sub(r'<[^>]+>', '', content); content = re.sub(r'\n{3,}', '\n\n', content).strip()
                        return content, True
            time.sleep(1 * (retry + 1))
        except Exception as e: print(f"  请求失败: {e}, 重试第{retry+1}次..."); time.sleep(1 * (retry + 1))
    return content, False
def sanitize_filename(filename):
    illegal = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for i in range(len(illegal)): filename = filename.replace(illegal[i], '')
    return filename
def down_book(it, chapter_range=""):
    name, chapters, zt = down_zj(it)
    if name == 'err': return 'err'
    zt = zt[0] if zt else ''
    safe_name = sanitize_filename(name + chapter_range)
    print(f'\n开始下载《{name}》，状态：{zt}'); print(f'共 {len(chapters)} 章')
    book_json_path = os.path.join(bookstore_dir, safe_name + '.json')
    cached = {}
    if os.path.exists(book_json_path):
        with open(book_json_path, 'r', encoding='UTF-8') as f: cached = json.load(f)
    import concurrent.futures; results = {}; results_lock = __import__('threading').Lock(); save_counter = [0]
    def download_one(title, cid):
        if title in cached:
            cached_val = cached[title]
            if isinstance(cached_val, str) and len(cached_val) > 50: return title, cached_val
        content, ok = down_text(cid)
        time.sleep(random.randint(config['delay'][0], config['delay'][1]) / 1000)
        if ok:
            with results_lock:
                cached[title] = content; save_counter[0] += 1
                if save_counter[0] >= 5:
                    save_counter[0] = 0
                    with open(book_json_path, 'w', encoding='UTF-8') as f: json.dump(cached, f, ensure_ascii=False)
            return title, content
        return title, ''
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=config.get('xc', 1)); futures = []; total = len(chapters)
    pbar = tqdm(total=total, desc='下载进度', unit='章', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}, {remaining}]')
    for title, cid in chapters.items(): futures.append(executor.submit(download_one, title, cid))
    for future in concurrent.futures.as_completed(futures):
        title, content = future.result(); results[title] = content; pbar.update(1)
    pbar.close(); executor.shutdown(wait=True)
    with open(book_json_path, 'w', encoding='UTF-8') as f: json.dump(cached, f, ensure_ascii=False)
    url = f'https://fanqienovel.com/page/{it}'; response = session.get(url); soup = BeautifulSoup(response.text, 'html.parser')
    author_name = None; author_el = soup.find('div', class_='author-name')
    if author_el:
        span = author_el.find('span', class_='author-name-text')
        if span: author_name = span.get_text(strip=True)
    description = None; desc_el = soup.find('div', class_='page-abstract-content')
    if desc_el:
        p = desc_el.find('p')
        if p: description = p.get_text(strip=True)
    fg = '\n' + config['kgf'] * config['kg']
    save_path = config['save_path'] if config['save_path'] else script_dir
    if save_path and not os.path.exists(save_path):
        try: os.makedirs(save_path, exist_ok=True)
        except Exception: print('保存路径不可用，回退到脚本目录: {}'.format(script_dir)); save_path = script_dir
    if config['save_mode'] == 1:
        txt_path = os.path.join(save_path, safe_name + '.txt')
        with open(txt_path, 'w', encoding='UTF-8') as f:
            f.write('小说名：{}\n作者：{}\n内容简介：{}\n'.format(name, author_name or '未知', description or '无'))
            f.write('共{}章  状态：{}\n'.format(len(chapters), zt or '未知'))
            if config.get('enable_toc', True):
                f.write('\n' + '=' * 50 + '\n目录\n' + '=' * 50 + '\n')
                for i, title in enumerate(chapters): f.write('{}. {}\n'.format(i + 1, title))
            f.write('\n' + '=' * 50 + '\n正文\n' + '=' * 50 + '\n')
            for i, title in enumerate(chapters):
                content = cached.get(title, '')
                prefix = ''
                if config.get('enable_chapter_numbering', False): prefix = '第{}章 '.format(i + 1)
                f.write('\n' + prefix + title + fg)
                if config['kg'] == 0: f.write(content + '\n')
                else: f.write(content.replace('\n', fg) + '\n')
        print('\n保存完成: {}'.format(txt_path))
    elif config['save_mode'] == 2:
        txt_dir = os.path.join(save_path, safe_name)
        if not os.path.exists(txt_dir): os.makedirs(txt_dir)
        for idx, title in enumerate(chapters):
            content = cached.get(title, '')
            fname = sanitize_filename(title) + '.txt' if not config.get('enable_chapter_numbering', False) else sanitize_filename(f"第{idx+1}章 {title}") + '.txt'
            fpath = os.path.join(txt_dir, fname)
            with open(fpath, 'w', encoding='UTF-8') as f:
                f.write(fg)
                if config['kg'] == 0: f.write(content + '\n')
                else: f.write(content.replace('\n', fg) + '\n')
        print(f'\n分章保存完成: {txt_dir}')
    try:
        with open(record_path, 'r', encoding='UTF-8') as f: records = json.load(f)
        entry = {'book_id': str(it), 'name': name, 'time': time.strftime('%Y-%m-%d %H:%M')}
        already = False
        for r in records:
            if isinstance(r, dict) and r.get('book_id') == str(it): already = True; break
        if not already: records.append(entry)
        with open(record_path, 'w', encoding='UTF-8') as f: json.dump(records, f, ensure_ascii=False)
    except: pass
    return 's'
SEARCH_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
_search_session = None
def _get_search_session():
    global _search_session
    if _search_session is None:
        _search_session = req.Session()
        _search_session.headers.update({'User-Agent': SEARCH_UA, 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Referer': 'https://fanqienovel.com/search', 'Connection': 'keep-alive'})
    return _search_session
def search_book():
    while True:
        key = input('\n请输入搜索关键词（直接回车返回）: ').strip()
        if not key: return None
        print('正在搜索「{}」...'.format(key))
        try:
            import urllib.parse as _urlparse
            params_dict = {'filter': '127,127,127,127', 'page_count': '10', 'page_index': '0', 'query_type': '0', 'query_word': key}
            query_string = _urlparse.urlencode(params_dict)
            try:
                from abogus import ABogus, BrowserFingerprintGenerator
                fp = BrowserFingerprintGenerator.generate_fingerprint("Chrome")
                ab = ABogus(user_agent=SEARCH_UA, fp=fp)
                result = ab.generate_abogus(params=query_string, request='GET')
                full_params = result[0]
            except ImportError: print('搜索功能需要 abogus.py 和 gmssl 库'); return None
            url = 'https://fanqienovel.com/api/author/search/search_book/v1?' + full_params
            search_sess = _get_search_session(); response = search_sess.get(url, timeout=config.get('timeout', 10))
            if response.status_code != 200: print('搜索请求失败'); continue
            if not response.text: print('搜索无响应'); continue
            data = response.json()
            if data.get('code') != 0: print('搜索出错'); continue
            books = data.get('data', {}).get('search_book_data_list', [])
            if not books: print('没有找到相关书籍。'); continue
            print('\n--- 搜索结果 ---'); results = []
            for i, book in enumerate(books):
                book_name = str_interpreter(str_interpreter(book.get('book_name', '未知'), 0), 1)
                author = str_interpreter(str_interpreter(book.get('author', '未知'), 0), 1)
                book_id = book.get('book_id', ''); word_count = book.get('word_count', 0)
                wc_str = '{}万字'.format(int(word_count) // 10000) if word_count and int(word_count) > 10000 else '{}字'.format(word_count)
                print('{}. 《{}》 作者：{}  {}'.format(i + 1, book_name, author, wc_str))
                results.append((book_id, book_name, author))
            print('---------------')
            while True:
                choice = input('\n输入序号下载，输入 v 查看详情，输入 r 重新搜索，输入 b 返回: ').strip()
                if choice.lower() == 'b': return None
                elif choice.lower() == 'r': break
                elif choice.lower() == 'v':
                    sel = input('输入序号查看详情: ').strip()
                    if sel.isdigit() and 1 <= int(sel) <= len(results): show_book_detail(results[int(sel) - 1][0])
                    else: print('序号无效')
                elif choice.isdigit() and 1 <= int(choice) <= len(results): return results[int(choice) - 1][0]
                else: print('输入无效，请重新输入。')
        except Exception as e: print('搜索出错: {}'.format(e)); continue
def parse_book_id(inp):
    inp = str(inp).strip()
    if 'book_id=' in inp:
        import urllib.parse as _urlparse
        try: parsed = _urlparse.parse_qs(inp.split('?', 1)[-1]); return parsed.get('book_id', [''])[0]
        except: pass
    if 'fanqienovel.com/page/' in inp: return inp.split('/page/')[-1].split('?')[0].split('/')[0]
    try: return str(int(inp))
    except: return None
def get_book_detail(book_id):
    url = 'https://fanqienovel.com/page/' + str(book_id)
    try: response = session.get(url, timeout=config.get('timeout', 10))
    except Exception as e: print('请求失败: {}'.format(e)); return None
    if response.status_code != 200: print('请求失败'); return None
    text = response.text; start_marker = 'window.__INITIAL_STATE__='; start_idx = text.find(start_marker)
    if start_idx == -1: return None
    start_idx += len(start_marker); depth = 0; in_string = False; escape = False; end_idx = start_idx
    for i in range(start_idx, len(text)):
        c = text[i]
        if escape: escape = False; continue
        if c == '\\': escape = True; continue
        if c == '"': in_string = not in_string; continue
        if in_string: continue
        if c == '{': depth += 1
        elif c == '}': depth -= 1
        if depth == 0: end_idx = i + 1; break
    try:
        raw = text[start_idx:end_idx]; raw = raw.replace(':undefined', ':null').replace(',undefined', ',null')
        state = json.loads(raw); p = state.get('page', {})
        categories = []; cat_v2 = p.get('categoryV2', '')
        if cat_v2 and isinstance(cat_v2, str):
            try:
                for c in json.loads(cat_v2):
                    if isinstance(c, dict) and c.get('Name'): categories.append(c['Name'])
            except: pass
        last_time = ''; lpt = p.get('lastPublishTime', '')
        if lpt:
            try: last_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(lpt)))
            except: last_time = str(lpt)
        return {'bookName': p.get('bookName', '未知'), 'author': p.get('author', '未知'), 'authorId': p.get('authorId', ''), 'wordNumber': p.get('wordNumber', 0), 'readCount': p.get('readCount', 0), 'chapterTotal': p.get('chapterTotal', 0), 'creationStatus': p.get('creationStatus', ''), 'lastChapterTitle': p.get('lastChapterTitle', ''), 'lastPublishTime': last_time, 'abstract': p.get('abstract', ''), 'description': p.get('description', ''), 'categories': categories, 'bookId': p.get('bookId', str(book_id))}
    except: return None
def show_book_detail(book_id):
    print('\n正在获取书籍信息...'); detail = get_book_detail(book_id)
    if not detail: print('获取书籍信息失败'); return None
    status_str = '已完结' if detail['creationStatus'] in (0, '0') else '连载中'
    word_count = int(detail['wordNumber'] or 0); read_count = int(detail['readCount'] or 0)
    wc_str = '{:.1f}万字'.format(word_count / 10000) if word_count >= 10000 else '{}字'.format(word_count)
    rc_str = '{:.1f}万'.format(read_count / 10000) if read_count >= 10000 else str(read_count)
    cat_str = '、'.join(detail['categories']) if detail['categories'] else '未分类'
    print('\n' + '=' * 50); print('《{}》'.format(detail['bookName'])); print('=' * 50)
    print('  作者：{}'.format(detail['author'])); print('  状态：{}'.format(status_str))
    print('  分类：{}'.format(cat_str)); print('  字数：{}'.format(wc_str))
    print('  章节数：{}'.format(detail['chapterTotal'])); print('  在读人数：{}'.format(rc_str))
    print('  最近更新：{}'.format(detail['lastChapterTitle'])); print('  更新时间：{}'.format(detail['lastPublishTime']))
    if detail['description']: print('  作者简介：{}'.format(detail['description'][:80]))
    if detail['abstract']:
        ab = detail['abstract'][:200]
        if len(detail['abstract']) > 200: ab += '...'
        print('\n  作品简介：'); print('  ' + ab.replace('\n', '\n  '))
    print('=' * 50)
    while True:
        choice = input('\n输入 d 下载该书，输入 b 返回: ').strip().lower()
        if choice == 'd': return detail['bookId']
        elif choice == 'b': return None
        else: print('输入无效')
def main():
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        if args[0] == '--book_id' and len(args) >= 2:
            status = down_book(args[1])
            if status == 'err': print('下载失败'); sys.exit(1)
            sys.exit(0)
        elif args[0] == '--check' and len(args) >= 2:
            detail = get_book_detail(args[1])
            if detail: print(json.dumps(detail, ensure_ascii=False))
            else: print('获取失败'); sys.exit(1)
            sys.exit(0)
        elif args[0] == '--search' and len(args) >= 2:
            keyword = args[1]
            try:
                import urllib.parse as _urlparse
                from abogus import ABogus, BrowserFingerprintGenerator
                params_dict = {'filter': '127,127,127,127', 'page_count': '10', 'page_index': '0', 'query_type': '0', 'query_word': keyword}
                query_string = _urlparse.urlencode(params_dict)
                fp = BrowserFingerprintGenerator.generate_fingerprint("Chrome")
                ab = ABogus(user_agent=SEARCH_UA, fp=fp)
                result = ab.generate_abogus(params=query_string, request='GET')
                full_params = result[0]
                url = 'https://fanqienovel.com/api/author/search/search_book/v1?' + full_params
                search_sess = _get_search_session(); response = search_sess.get(url, timeout=config.get('timeout', 10))
                if response.status_code == 200 and response.text:
                    data = response.json()
                    if data.get('code') == 0:
                        books = data.get('data', {}).get('search_book_data_list', [])
                        results = []
                        for book in books:
                            book_name = str_interpreter(str_interpreter(book.get('book_name', '未知'), 0), 1)
                            author = str_interpreter(str_interpreter(book.get('author', '未知'), 0), 1)
                            results.append({'book_name': book_name, 'author': author, 'book_id': book.get('book_id', ''), 'word_count': book.get('word_count', 0)})
                        print(json.dumps(results, ensure_ascii=False, indent=2)); sys.exit(0)
                print('搜索失败'); sys.exit(1)
            except Exception as e: print('搜索出错: {}'.format(e)); sys.exit(1)
        else:
            print('用法: python3 fanqie_txt.py --book_id <id>'); print('      python3 fanqie_txt.py --check <book_id>'); print('      python3 fanqie_txt.py --search <keyword>'); sys.exit(1)
    print(); print('╔' + '═' * 48 + '╗')
    print('║' + '  🍅 番茄小说下载器 v3.0  @小哲'.ljust(46) + '║')
    print('╠' + '═' * 48 + '╣')
    save_path_display = config.get('save_path', '未设置')
    if len(save_path_display) > 40: save_path_display = '...' + save_path_display[-37:]
    print('║' + f'  📁 保存: {save_path_display}'.ljust(46) + '║')
    print('╠' + '═' * 48 + '╣')
    print('║' + '  📖 输入 book_id/链接 → 直接下载'.ljust(46) + '║')
    print('║' + '  🔍 ss → 搜索小说'.ljust(46) + '║')
    print('║' + '  📊 ph → 浏览榜单'.ljust(46) + '║')
    print('║' + '  ℹ️  vd → 查看图书详情'.ljust(46) + '║')
    print('║' + '  📚 bd → 批量下载'.ljust(46) + '║')
    print('║' + '  🛠️  t  → 工具箱'.ljust(46) + '║')
    print('║' + '  ⚙️  s  → 设置'.ljust(46) + '║')
    print('║' + '  🚪 q  → 退出'.ljust(46) + '║')
    print('╚' + '═' * 48 + '╝'); print()
    while True:
        inp = input('\n请输入: ').strip()
        if not inp: continue
        if inp.lower() == 'q': print('再见！'); break
        if inp.lower() == 'ss':
            book_id = search_book()
            if book_id: print('书籍 ID: {}'.format(book_id)); status = down_book(book_id)
            if status == 'err': print('下载失败')
            continue
        if inp.lower() == 'ph':
            book_id = show_rank()
            if book_id: print('书籍 ID: {}'.format(book_id)); status = down_book(book_id)
            if status == 'err': print('下载失败')
            continue
        if inp.lower() == 'vd':
            inp2 = input('请输入书籍 ID 或链接: ').strip(); bid = parse_book_id(inp2)
            if bid:
                book_id = show_book_detail(bid)
                if book_id: print('书籍 ID: {}'.format(book_id)); status = down_book(book_id)
                if status == 'err': print('下载失败')
            else: print('无法识别书籍 ID')
            continue
        if inp.lower() == 's':
            print('\n--- 设置 ---')
            print('1. 段首缩进空格数 (当前: {})'.format(config['kg']))
            print('2. 保存路径 (当前: {})'.format(config.get('save_path', '未设置')))
            print('3. 下载模式 (当前: {})'.format('单个TXT' if config['save_mode'] == 1 else '分章TXT'))
            print('4. 线程数 (当前: {})'.format(config['xc']))
            inp3 = input('选择 (1-4, b返回): ').strip()
            if inp3 == '1':
                try: v = int(input('缩进空格数 (0-8): ')); config['kg'] = max(0, min(8, v))
                except: pass
            elif inp3 == '2': config.select_save_path()
            elif inp3 == '3': config['save_mode'] = 2 if config['save_mode'] == 1 else 1; print('下载模式已切换为:', '单个TXT' if config['save_mode'] == 1 else '分章TXT')
            elif inp3 == '4':
                try: v = int(input('线程数 (1-5): ')); config['xc'] = max(1, min(5, v))
                except: pass
            continue
        bid = parse_book_id(inp)
        if bid:
            book_id = bid; print('书籍 ID: {}'.format(book_id)); status = down_book(book_id)
            if status == 'err': print('下载失败，请检查书籍 ID 是否正确')
        else: print('无法识别，输入 ss 搜索，ph 浏览榜单，vd 查看详情')
if __name__ == '__main__': main()
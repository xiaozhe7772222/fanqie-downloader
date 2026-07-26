# -*- coding: utf-8 -*-
"""
番茄小说下载器 - 精简版（仅TXT）
依赖: requests, beautifulsoup4, tqdm, gmssl
适配 Pydroid 3: 已移除 lxml, ebooklib, qrcode, flask 等重型依赖
"""
import requests as req
from bs4 import BeautifulSoup
from tqdm import tqdm
import json, time, random, os, sys, re

# ==================== 字符解密表 ====================
CODE = [[58344, 58715], [58345, 58716]]
charset = json.loads(
    '[["D","在","主","特","家","军","然","表","场","4","要","只","v","和","?","6","别","还","g","现","儿","岁","?","?","此","象","月","3","出","战","工","相","o","男","直","失","世","F","都","平","文","什","V","O","将","真","T","那","当","?","会","立","些","u","是","十","张","学","气","大","爱","两","命","全","后","东","性","通","被","1","它","乐","接","而","感","车","山","公","了","常","以","何","可","话","先","p","i","叫","轻","M","士","w","着","变","尔","快","l","个","说","少","色","里","安","花","远","7","难","师","放","t","报","认","面","道","S","?","克","地","度","I","好","机","U","民","写","把","万","同","水","新","没","书","电","吃","像","斯","5","为","y","白","几","日","教","看","但","第","加","候","作","上","拉","住","有","法","r","事","应","位","利","你","声","身","国","问","马","女","他","Y","比","父","x","A","H","N","s","X","边","美","对","所","金","活","回","意","到","z","从","j","知","又","内","因","点","Q","三","定","8","R","b","正","或","夫","向","德","听","更","?","得","告","并","本","q","过","记","L","让","打","f","人","就","者","去","原","满","体","做","经","K","走","如","孩","c","G","给","使","物","?","最","笑","部","?","员","等","受","k","行","一","条","果","动","光","门","头","见","往","自","解","成","处","天","能","于","名","其","发","总","母","的","死","手","入","路","进","心","来","h","时","力","多","开","已","许","d","至","由","很","界","n","小","与","Z","想","代","么","分","生","口","再","妈","望","次","西","风","种","带","J","?","实","情","才","这","?","E","我","神","格","长","觉","间","年","眼","无","不","亲","关","结","0","友","信","下","却","重","己","老","2","音","字","m","呢","明","之","前","高","P","B","目","太","e","9","起","稜","她","也","W","用","方","子","英","每","理","便","四","数","期","中","C","外","样","a","海","们","任"],["s","?","作","口","在","他","能","并","B","士","4","U","克","才","正","们","字","声","高","全","尔","活","者","动","其","主","报","多","望","放","h","w","次","年","?","中","3","特","于","十","入","要","男","同","G","面","分","方","K","什","再","教","本","己","结","1","等","世","N","?","说","g","u","期","Z","外","美","M","行","给","9","文","将","两","许","张","友","0","英","应","向","像","此","白","安","少","何","打","气","常","定","间","花","见","孩","它","直","风","数","使","道","第","水","已","女","山","解","d","P","的","通","关","性","叫","儿","L","妈","问","回","神","来","S","","四","望","前","国","些","O","v","l","A","心","平","自","无","军","光","代","是","好","却","c","得","种","就","意","先","立","z","子","过","Y","j","表","","么","所","接","了","名","金","受","J","满","眼","没","部","那","m","每","车","度","可","R","斯","经","现","门","明","V","如","走","命","y","6","E","战","很","上","f","月","西","7","长","夫","想","话","变","海","机","x","到","W","一","成","生","信","笑","但","父","开","内","东","马","日","小","而","后","带","以","三","几","为","认","X","死","员","目","位","之","学","远","人","音","呢","我","q","乐","象","重","对","个","被","别","F","也","书","稜","D","写","还","因","家","发","时","i","或","住","德","当","o","l","比","觉","然","吃","去","公","a","老","亲","情","体","太","b","万","C","电","理","?","失","力","更","拉","物","着","原","她","工","实","色","感","记","看","出","相","路","大","你","候","2","和","?","与","p","样","新","只","便","最","不","进","T","r","做","格","母","总","爱","身","师","轻","知","往","加","从","?","天","e","H","?","听","场","由","快","边","让","把","任","8","条","头","事","至","起","点","真","手","这","难","都","界","用","法","n","处","下","又","Q","告","地","5","k","t","岁","有","会","果","利","民"]]'
)

# ==================== 配置 ====================
class Config:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            self.script_dir = os.path.dirname(sys.executable)
        else:
            self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.script_dir, 'data')
        self.bookstore_dir = os.path.join(self.data_dir, 'bookstore')
        self.config_path = os.path.join(self.data_dir, 'config.json')
        self.default_config = {
            'kg': 2,
            'kgf': '\u3000',          # 全角空格
            'delay': [50, 150],
            'save_path': '',  # 空=自动检测，首次运行会提示选择
            'save_mode': 1,           # 1=单个txt, 2=分章txt
            'xc': 1,                  # 线程数
            'enable_chapter_numbering': False,
            'max_retries': 3,
            'timeout': 10,
            'version': '2.1.0-lite',
        }
        if not os.path.exists(self.data_dir):
            self.config = self.default_config.copy()
            self._detect_save_path()
        else:
            self.config = self.load_config()
            if not self.config.get('save_path'):
                self._detect_save_path()

    def create_directories(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.bookstore_dir):
            os.makedirs(self.bookstore_dir)
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w', encoding='UTF-8') as f:
                json.dump(self.default_config, f, indent=2, ensure_ascii=False)
        record_path = os.path.join(self.data_dir, 'record.json')
        if not os.path.exists(record_path):
            with open(record_path, 'w', encoding='UTF-8') as f:
                json.dump([], f)

    def __getitem__(self, key):
        try:
            return self.config[key]
        except (KeyError, TypeError):
            if isinstance(key, str) and key in self.default_config:
                return self.default_config[key]
            return None

    def __setitem__(self, key, value):
        self.config[key] = value
        self.save_config()

    def load_config(self):
        if not os.path.exists(self.data_dir):
            return self.default_config.copy()
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='UTF-8') as f:
                try:
                    config = json.load(f)
                    merged = self.default_config.copy()
                    merged.update(config)
                    return merged
                except json.JSONDecodeError:
                    return self.default_config.copy()
        return self.default_config.copy()

    def save_config(self):
        if os.path.exists(self.data_dir):
            with open(self.config_path, 'w', encoding='UTF-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)

    def _detect_save_path(self):
        """自动检测Android可写存储路径"""
        candidates = [
            '/storage/emulated/0/番茄小说下载/',
            '/sdcard/番茄小说下载/',
            '/storage/self/primary/番茄小说下载/',
            os.path.join(self.script_dir, 'downloads'),
        ]
        for p in candidates:
            try:
                os.makedirs(p, exist_ok=True)
                test_file = os.path.join(p, '.write_test')
                with open(test_file, 'w') as f:
                    f.write('1')
                os.remove(test_file)
                self.config['save_path'] = p
                self.save_config()
                print(f'📁 保存路径已自动设为: {p}')
                return
            except Exception:
                continue
        # 都失败则回退到脚本目录
        fallback = os.path.join(self.script_dir, 'downloads')
        os.makedirs(fallback, exist_ok=True)
        self.config['save_path'] = fallback
        self.save_config()
        print(f'📁 保存路径已自动设为: {fallback}')

    def select_save_path(self):
        """让用户选择保存路径"""
        print('\n' + '=' * 50)
        print('  📂 选择保存路径')
        print('=' * 50)
        print(f'  当前路径: {self.config.get("save_path", "未设置")}')
        print()
        print('  1. 使用默认路径 (/storage/emulated/0/番茄小说下载/)')
        print('  2. 手动输入路径')
        print('  3. 使用脚本目录下的 downloads 文件夹')
        print('  b. 返回')
        print()
        choice = input('  请选择 (1/2/3/b): ').strip()
        if choice == '1':
            p = '/storage/emulated/0/番茄小说下载/'
            try:
                os.makedirs(p, exist_ok=True)
                self.config['save_path'] = p
                self.save_config()
                print(f'  ✅ 已设置为: {p}')
            except Exception:
                print('  ❌ 该路径不可写，请尝试其他选项')
        elif choice == '2':
            p = input('  请输入保存路径: ').strip()
            if p:
                try:
                    os.makedirs(p, exist_ok=True)
                    test_file = os.path.join(p, '.write_test')
                    with open(test_file, 'w') as f:
                        f.write('1')
                    os.remove(test_file)
                    self.config['save_path'] = p
                    self.save_config()
                    print(f'  ✅ 已设置为: {p}')
                except Exception:
                    print('  ❌ 路径不可写，请检查权限')
            else:
                print('  ❌ 路径不能为空')
        elif choice == '3':
            p = os.path.join(self.script_dir, 'downloads')
            os.makedirs(p, exist_ok=True)
            self.config['save_path'] = p
            self.save_config()
            print(f'  ✅ 已设置为: {p}')
        else:
            print('  已取消')
        return

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()


config = Config()
config.create_directories()

script_dir   = config.script_dir
data_dir     = config.data_dir
bookstore_dir = config.bookstore_dir
record_path  = os.path.join(data_dir, 'record.json')

# ==================== 网络请求 ====================
headers_lib = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47',
]

session = req.Session()
session.mount('http://', req.adapters.HTTPAdapter(max_retries=3))
session.mount('https://', req.adapters.HTTPAdapter(max_retries=3))
session.headers.update({
    'User-Agent': random.choice(headers_lib),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
})


# ==================== 字符解密 ====================
def interpreter(uni, mode):
    bias = uni - CODE[mode][0]
    if bias < 0 or bias >= len(charset[mode]) or charset[mode][bias] == '?':
        return chr(uni)
    return charset[mode][bias]


def str_interpreter(n, mode):
    s = ''
    for ch in n:
        uni = ord(ch)
        if CODE[mode][0] <= uni <= CODE[mode][1]:
            s += interpreter(uni, mode)
        else:
            s += ch
    return s


# ==================== 获取书籍信息（用 BeautifulSoup 替代 lxml） ====================
def down_zj(it):
    """获取书名和章节列表，返回 [书名, {章节标题: 章节ID}, 状态]"""
    url = 'https://fanqienovel.com/page/' + str(it)
    response = session.get(url, timeout=config.get('timeout', 10))
    if response.status_code != 200:
        print(f"网络请求失败，状态码: {response.status_code}")
        return ['err', {}, []]

    soup = BeautifulSoup(response.text, 'html.parser')

    # 书名
    h1 = soup.find('h1')
    if not h1:
        return ['err', {}, []]
    name = h1.get_text(strip=True)

    # 章节列表
    chapters = {}
    chapter_divs = soup.find_all('div', class_='chapter')
    for cdiv in chapter_divs:
        links = cdiv.find_all('a')
        for a in links:
            title = a.get_text(strip=True)
            href = a.get('href', '')
            cid = href.split('/')[-1]
            if title and cid:
                chapters[title] = cid

    # 状态
    status_text = ''
    status_span = soup.find('span', class_='info-label-yellow')
    if status_span:
        status_text = status_span.get_text(strip=True)

    return [name, chapters, [status_text]]


# ==================== 下载章节正文 ====================
def down_text(it):
    """下载单章正文并解密，返回 (content, success)"""
    max_retries = config.get('max_retries', 3)
    content = ""
    for retry in range(max_retries):
        try:
            response = session.get(
                f"https://fanqienovel.com/reader/{it}",
                timeout=config.get('timeout', 10)
            )
            if response.status_code == 200:
                text = response.text
                start_marker = 'window.__INITIAL_STATE__='
                start_idx = text.find(start_marker)
                if start_idx != -1:
                    start_idx += len(start_marker)
                    depth = 0
                    in_string = False
                    escape = False
                    end_idx = start_idx
                    for i in range(start_idx, len(text)):
                        c = text[i]
                        if escape:
                            escape = False
                            continue
                        if c == '\\':
                            escape = True
                            continue
                        if c == '"':
                            in_string = not in_string
                            continue
                        if in_string:
                            continue
                        if c == '{':
                            depth += 1
                        elif c == '}':
                            depth -= 1
                            if depth == 0:
                                end_idx = i + 1
                                break
                    raw_json = text[start_idx:end_idx]
                    state = json.loads(raw_json)
                    content = state.get('reader', {}).get('chapterData', {}).get('content', '')
                    if content:
                        content = str_interpreter(content, 0)
                        content = re.sub(r'<header>.*?</header>', '', content, flags=re.DOTALL)
                        content = re.sub(r'<footer>.*?</footer>', '', content, flags=re.DOTALL)
                        content = re.sub(r'</?article>', '', content)
                        content = re.sub(r'<p idx="\d+">', '\n', content)
                        content = re.sub(r'</p>', '\n', content)
                        content = re.sub(r'<[^>]+>', '', content)
                        content = re.sub(r'\n{3,}', '\n\n', content).strip()
                        return content, True
            time.sleep(1 * (retry + 1))
        except Exception as e:
            print(f"  请求失败: {e}, 重试第{retry+1}次...")
            time.sleep(1 * (retry + 1))
    return content, False


# ==================== 文件名净化 ====================
def sanitize_filename(filename):
    illegal = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    replace = ['＜', '＞', '：', '＂', '／', '＼', '｜', '？', '＊']
    for i in range(len(illegal)):
        filename = filename.replace(illegal[i], replace[i])
    return filename


# ==================== 下载整本书 ====================
def down_book(it, chapter_range=""):
    """下载整本书并保存为 TXT"""
    name, chapters, zt = down_zj(it)
    if name == 'err':
        return 'err'

    zt = zt[0] if zt else ''
    safe_name = sanitize_filename(name + chapter_range)
    print(f'\n开始下载《{name}》，状态：{zt}')
    print(f'共 {len(chapters)} 章')

    # 断点续传：加载已有缓存
    book_json_path = os.path.join(bookstore_dir, safe_name + '.json')
    cached = {}
    if os.path.exists(book_json_path):
        with open(book_json_path, 'r', encoding='UTF-8') as f:
            cached = json.load(f)

    # 多线程下载
    import concurrent.futures
    results = {}
    results_lock = __import__('threading').Lock()
    save_counter = [0]

    def download_one(title, cid):
        if title in cached:
            cached_val = cached[title]
            if isinstance(cached_val, str) and len(cached_val) > 50:
                return title, cached_val
        content, ok = down_text(cid)
        time.sleep(random.randint(config['delay'][0], config['delay'][1]) / 1000)
        if ok:
            with results_lock:
                cached[title] = content
                save_counter[0] += 1
                if save_counter[0] >= 5:
                    save_counter[0] = 0
                    with open(book_json_path, 'w', encoding='UTF-8') as f:
                        json.dump(cached, f, ensure_ascii=False)
            return title, content
        return title, ''

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=config.get('xc', 1))
    futures = []
    total = len(chapters)
    done_count = [0]
    pbar = tqdm(total=total, desc='下载进度', unit='章',
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}, {remaining}]')
    for title, cid in chapters.items():
        futures.append(executor.submit(download_one, title, cid))
    for future in concurrent.futures.as_completed(futures):
        title, content = future.result()
        results[title] = content
        done_count[0] += 1
        pbar.set_postfix_str(title[:20])
        pbar.update(1)
    pbar.close()
    executor.shutdown(wait=True)

    # 最终保存缓存
    with open(book_json_path, 'w', encoding='UTF-8') as f:
        json.dump(cached, f, ensure_ascii=False)

    # 获取作者和简介
    url = f'https://fanqienovel.com/page/{it}'
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    author_name = None
    author_el = soup.find('div', class_='author-name')
    if author_el:
        span = author_el.find('span', class_='author-name-text')
        if span:
            author_name = span.get_text(strip=True)
    description = None
    desc_el = soup.find('div', class_='page-abstract-content')
    if desc_el:
        p = desc_el.find('p')
        if p:
            description = p.get_text(strip=True)

    # 写入 TXT
    fg = '\n' + config['kgf'] * config['kg']
    save_path = config['save_path'] if config['save_path'] else script_dir
    # 安卓路径不存在时回退到脚本目录
    if save_path and not os.path.exists(save_path):
        try:
            os.makedirs(save_path, exist_ok=True)
        except Exception:
            print('保存路径不可用，回退到脚本目录: {}'.format(script_dir))
            save_path = script_dir

    if config['save_mode'] == 1:
        # 单个 TXT
        txt_path = os.path.join(save_path, safe_name + '.txt')
        with open(txt_path, 'w', encoding='UTF-8') as f:
            f.write('小说名：{}\n作者：{}\n内容简介：{}\n'.format(name, author_name or '未知', description or '无'))
            f.write('共{}章  状态：{}\n'.format(len(chapters), zt or '未知'))
            # 目录
            if config.get('enable_toc', True):
                f.write('\n' + '=' * 50 + '\n目录\n' + '=' * 50 + '\n')
                for i, title in enumerate(chapters):
                    f.write('{}. {}\n'.format(i + 1, title))
            f.write('\n' + '=' * 50 + '\n正文\n' + '=' * 50 + '\n')
            for i, title in enumerate(chapters):
                content = cached.get(title, '')
                prefix = ''
                if config.get('enable_chapter_numbering', False):
                    prefix = '第{}章 '.format(i + 1)
                f.write('\n' + prefix + title + fg)
                if config['kg'] == 0:
                    f.write(content + '\n')
                else:
                    f.write(content.replace('\n', fg) + '\n')
        print('\n保存完成: {}'.format(txt_path))
    elif config['save_mode'] == 2:
        # 分章 TXT
        txt_dir = os.path.join(save_path, safe_name)
        if not os.path.exists(txt_dir):
            os.makedirs(txt_dir)
        for idx, title in enumerate(chapters):
            content = cached.get(title, '')
            if config.get('enable_chapter_numbering', False):
                fname = sanitize_filename(f"第{idx+1}章 {title}") + '.txt'
            else:
                fname = sanitize_filename(title) + '.txt'
            fpath = os.path.join(txt_dir, fname)
            with open(fpath, 'w', encoding='UTF-8') as f:
                f.write(fg)
                if config['kg'] == 0:
                    f.write(content + '\n')
                else:
                    f.write(content.replace('\n', fg) + '\n')
        print(f'\n分章保存完成: {txt_dir}')

    # 记录已下载
    try:
        with open(record_path, 'r', encoding='UTF-8') as f:
            records = json.load(f)
        entry = {'book_id': str(it), 'name': name, 'time': time.strftime('%Y-%m-%d %H:%M')}
        # 兼容旧格式
        already = False
        for r in records:
            if isinstance(r, dict) and r.get('book_id') == str(it):
                already = True
                break
            elif isinstance(r, str) and r == str(it):
                already = True
                break
        if not already:
            records.append(entry)
        with open(record_path, 'w', encoding='UTF-8') as f:
            json.dump(records, f, ensure_ascii=False)
    except Exception:
        pass

    return 's'


# ==================== 搜索功能 ====================
# 搜索API专用UA（必须与a_bogus生成时使用的UA完全一致，否则服务端验签失败）
SEARCH_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'

# 搜索专用session（独立于下载用的全局session，避免UA不一致导致a_bogus验签失败）
_search_session = None

def _get_search_session():
    """获取搜索专用session，懒加载"""
    global _search_session
    if _search_session is None:
        _search_session = req.Session()
        _search_session.headers.update({
            'User-Agent': SEARCH_UA,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://fanqienovel.com/search',
            'Connection': 'keep-alive',
        })
    return _search_session


def search_book():
    """搜索番茄小说，返回 book_id 或 None"""
    while True:
        key = input('\n请输入搜索关键词（直接回车返回）: ').strip()
        if not key:
            return None
        print('正在搜索「{}」...'.format(key))
        try:
            # 构造搜索API参数
            params_dict = {
                'filter': '127,127,127,127',
                'page_count': '10',
                'page_index': '0',
                'query_type': '0',
                'query_word': key,
            }
            import urllib.parse as _urlparse
            query_string = _urlparse.urlencode(params_dict)

            # 生成 a_bogus 参数绕过反爬（使用外部 abogus.py 模块）
            try:
                from abogus import ABogus, BrowserFingerprintGenerator
                fp = BrowserFingerprintGenerator.generate_fingerprint("Chrome")
                ab = ABogus(user_agent=SEARCH_UA, fp=fp)
                result = ab.generate_abogus(params=query_string, request='GET')
                full_params = result[0]
            except ImportError:
                print('搜索功能需要 abogus.py 和 gmssl 库，请确保已安装。')
                print('安装命令: pip install gmssl')
                return None

            url = 'https://fanqienovel.com/api/author/search/search_book/v1?' + full_params
            # 使用搜索专用session，确保UA与a_bogus一致
            search_sess = _get_search_session()
            response = search_sess.get(url, timeout=config.get('timeout', 10))
            if response.status_code != 200:
                print('搜索请求失败，状态码: {}'.format(response.status_code))
                continue
            if not response.text:
                print('搜索无响应，可能被反爬拦截，请稍后重试。')
                continue
            data = response.json()
            if data.get('code') != 0:
                print('搜索出错，错误码: {}'.format(data.get('code')))
                continue
            books = data.get('data', {}).get('search_book_data_list', [])
            if not books:
                print('没有找到相关书籍。')
                continue
            print('\n--- 搜索结果 ---')
            results = []
            for i, book in enumerate(books):
                book_name = book.get('book_name', '未知')
                author = book.get('author', '未知')
                book_id = book.get('book_id', '')
                word_count = book.get('word_count', 0)
                if word_count and int(word_count) > 10000:
                    wc_str = '{}万字'.format(int(word_count) // 10000)
                else:
                    wc_str = '{}字'.format(word_count)
                # 解密搜索结果中的加密字符（尝试两种模式）
                book_name = str_interpreter(book_name, 0)
                book_name = str_interpreter(book_name, 1)
                author = str_interpreter(author, 0)
                author = str_interpreter(author, 1)
                print('{}. 《{}》 作者：{}  {}'.format(i + 1, book_name, author, wc_str))
                results.append((book_id, book_name, author))
            print('---------------')
            while True:
                choice = input('\n输入序号下载，输入 v 查看详情，输入 r 重新搜索，输入 b 返回: ').strip()
                if choice.lower() == 'b':
                    return None
                elif choice.lower() == 'r':
                    break
                elif choice.lower() == 'v':
                    sel = input('输入序号查看详情: ').strip()
                    if sel.isdigit() and 1 <= int(sel) <= len(results):
                        show_book_detail(results[int(sel) - 1][0])
                    else:
                        print('序号无效')
                    continue
                elif choice.isdigit() and 1 <= int(choice) <= len(results):
                    return results[int(choice) - 1][0]
                else:
                    print('输入无效，请重新输入。')
        except Exception as e:
            print('搜索出错: {}'.format(e))
            continue


# ==================== 榜单功能 ====================
# 番茄小说榜单分类（从页面 __INITIAL_STATE__ 提取）
RANK_CATEGORIES = {
    'male': [
        ('1141', '西方奇幻'), ('1140', '东方仙侠'), ('8', '科幻末世'),
        ('261', '都市日常'), ('124', '都市修真'), ('1014', '都市高武'),
        ('273', '历史古代'), ('27', '战神赘婿'), ('263', '都市种田'),
        ('258', '传统玄幻'), ('272', '历史脑洞'), ('539', '悬疑脑洞'),
        ('262', '都市脑洞'), ('257', '玄幻脑洞'), ('751', '悬疑灵异'),
        ('504', '抗战谍战'), ('746', '游戏体育'), ('718', '动漫衍生'),
        ('1016', '男频衍生'),
    ],
    'female': [
        ('1139', '古风世情'), ('8', '科幻末世'), ('746', '游戏体育'),
        ('1015', '女频衍生'), ('248', '玄幻言情'), ('23', '种田'),
        ('79', '年代'), ('267', '现言脑洞'), ('246', '宫斗宅斗'),
        ('539', '悬疑脑洞'), ('253', '古言脑洞'), ('24', '快穿'),
        ('749', '青春甜宠'), ('745', '星光璀璨'), ('747', '女频悬疑'),
        ('750', '职场婚恋'), ('748', '豪门总裁'), ('1017', '民国言情'),
    ],
}

# 榜单类型: 0=阅读榜, 1=新书榜
RANK_TYPES = [('0', '阅读榜'), ('1', '新书榜')]


def fetch_rank(gender, category_id, rank_type=0, limit=100):
    """获取榜单数据，返回书籍列表。
    先从HTML页面获取前10本（支持所有榜单类型），
    再用API获取更多（仅阅读榜支持）。
    """
    import urllib.parse as _urlparse

    # 第一步：从HTML页面获取前10本
    rank_url = 'https://fanqienovel.com/rank/{}_{}_{}'.format(gender, rank_type, category_id)
    search_sess = _get_search_session()
    try:
        # 用搜索session但需要改Accept为HTML
        old_accept = search_sess.headers.get('Accept', '')
        search_sess.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        response = search_sess.get(rank_url, timeout=config.get('timeout', 10))
        search_sess.headers['Accept'] = old_accept
    except Exception as e:
        print('榜单页面请求失败: {}'.format(e))
        return []

    if response.status_code != 200:
        print('榜单页面请求失败，状态码: {}'.format(response.status_code))
        return []

    books = _extract_rank_from_html(response.text)

    # 第二步：如果需要更多且是阅读榜，用API获取剩余
    if len(books) >= 10 and limit > 10 and rank_type == 0:
        try:
            from abogus import ABogus, BrowserFingerprintGenerator
            all_books = list(books)
            offset = 10
            while offset < limit and offset < 100:
                params_dict = {
                    'app_id': '2503',
                    'rank_list_type': '3',
                    'offset': str(offset),
                    'limit': '10',
                    'category_id': str(category_id),
                    'rank_version': '',
                    'gender': str(gender),
                    'rankMold': '2',
                }
                query_string = _urlparse.urlencode(params_dict)
                fp = BrowserFingerprintGenerator.generate_fingerprint("Chrome")
                ab = ABogus(user_agent=SEARCH_UA, fp=fp)
                result = ab.generate_abogus(params=query_string, request='GET')
                full_params = result[0]

                api_url = 'https://fanqienovel.com/api/rank/category/list?' + full_params
                api_resp = search_sess.get(api_url, timeout=config.get('timeout', 10))
                search_sess.headers['Accept'] = old_accept
                if api_resp.status_code == 200 and api_resp.text:
                    data = api_resp.json()
                    more_books = data.get('data', {}).get('book_list', [])
                    if not more_books:
                        break
                    all_books.extend(more_books)
                    offset += 10
                else:
                    break
            books = all_books[:limit]
        except ImportError:
            pass  # 没有abogus也能用前10本
        except Exception as e:
            print('获取更多榜单数据失败: {}'.format(e))

    return books


def _extract_rank_from_html(html_text):
    """从榜单页面HTML中提取__INITIAL_STATE__中的书籍列表"""
    start_marker = 'window.__INITIAL_STATE__='
    start_idx = html_text.find(start_marker)
    if start_idx == -1:
        return []
    start_idx += len(start_marker)
    depth = 0
    in_string = False
    escape = False
    end_idx = start_idx
    for i in range(start_idx, len(html_text)):
        c = html_text[i]
        if escape:
            escape = False
            continue
        if c == '\\':
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                end_idx = i + 1
                break
    try:
        raw_json = html_text[start_idx:end_idx]
        # 修复JS中的undefined值（非合法JSON）
        raw_json = raw_json.replace(':undefined', ':null').replace(',undefined', ',null')
        state = json.loads(raw_json)
        return state.get('rank', {}).get('book_list', [])
    except (json.JSONDecodeError, ValueError):
        return []


def show_rank():
    """交互式浏览榜单，返回 book_id 或 None"""
    # 1. 选择频道
    print('\n--- 榜单浏览 ---')
    print('1. 男频')
    print('2. 女频')
    ch = input('选择频道 (1/2): ').strip()
    if ch == '1':
        gender = 1
        gender_name = '男频'
        cats = RANK_CATEGORIES['male']
    elif ch == '2':
        gender = 0
        gender_name = '女频'
        cats = RANK_CATEGORIES['female']
    else:
        print('输入无效')
        return None

    # 2. 选择榜单类型
    print('\n1. 阅读榜')
    print('2. 新书榜')
    tc = input('选择榜单类型 (1/2，默认1): ').strip() or '1'
    rank_type = 0 if tc == '1' else 1
    rank_type_name = '阅读榜' if rank_type == 0 else '新书榜'

    # 3. 选择分类
    print('\n{}{} 分类:'.format(gender_name, rank_type_name))
    for i, (cid, cname) in enumerate(cats):
        print('  {:2d}. {}'.format(i + 1, cname))
    cc = input('\n选择分类序号 (1-{}): '.format(len(cats))).strip()
    try:
        idx = int(cc) - 1
        if idx < 0 or idx >= len(cats):
            print('序号无效')
            return None
    except ValueError:
        print('输入无效')
        return None
    category_id, category_name = cats[idx]

    # 4. 获取榜单数据
    title = '{}{}·{}'.format(gender_name, rank_type_name, category_name)
    print('\n正在获取「{}」...'.format(title))
    books = fetch_rank(gender, category_id, rank_type=rank_type, limit=100)
    if not books:
        print('获取榜单失败或无数据')
        return None

    print('\n=== {} （共{}本）==='.format(title, len(books)))
    print('{:>4}  {:<22} {:<10} {:>8}  {:>8}'.format('排名', '书名', '作者', '字数', '在读'))
    print('-' * 70)
    results = []
    for b in books:
        pos = b.get('currentPos', '?')
        name = str_interpreter(str_interpreter(b.get('bookName', '未知'), 0), 1)
        author = str_interpreter(str_interpreter(b.get('author', '未知'), 0), 1)
        word_count = int(b.get('wordNumber', 0))
        read_count = int(b.get('read_count', 0))
        status = '已完结' if b.get('creationStatus') == '0' else '连载中'
        if word_count >= 10000:
            wc_str = '{:.1f}万'.format(word_count / 10000)
        else:
            wc_str = str(word_count)
        if read_count >= 10000:
            rc_str = '{:.1f}万'.format(read_count / 10000)
        else:
            rc_str = str(read_count)
        name_display = name[:20] + '..' if len(name) > 22 else name
        print('{:>4}  {:<22} {:<10} {:>8}  {:>8}  {}'.format(
            pos, name_display, author[:8], wc_str, rc_str, status))
        results.append((b.get('bookId', ''), name, author))

    # 5. 选择操作
    while True:
        choice = input('\n输入序号下载该书，输入 v 查看详情，输入 e 导出TXT，输入 c 导出CSV，输入 b 返回: ').strip()
        if choice.lower() == 'b':
            return None
        elif choice.lower() == 'e':
            export_rank(title, results)
            continue
        elif choice.lower() == 'c':
            export_rank_csv(title, books)
            continue
        elif choice.lower() == 'v':
            sel = input('输入序号查看详情: ').strip()
            if sel.isdigit() and 1 <= int(sel) <= len(results):
                show_book_detail(results[int(sel) - 1][0])
            else:
                print('序号无效')
            continue
        elif choice.isdigit() and 1 <= int(choice) <= len(results):
            return results[int(choice) - 1][0]
        else:
            print('输入无效')


def export_rank(title, results):
    """将榜单数据导出为TXT"""
    save_path = config['save_path'] if config['save_path'] else script_dir
    if save_path and not os.path.exists(save_path):
        try:
            os.makedirs(save_path, exist_ok=True)
        except Exception:
            save_path = script_dir
    safe_title = sanitize_filename(title)
    fpath = os.path.join(save_path, safe_title + '.txt')
    with open(fpath, 'w', encoding='UTF-8') as f:
        f.write('番茄小说榜单 - {}\n'.format(title))
        f.write('导出时间: {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
        f.write('=' * 60 + '\n\n')
        for i, (bid, name, author) in enumerate(results):
            f.write('{:3d}. 《{}》 作者：{}  ID:{}\n'.format(i + 1, name, author, bid))
    print('榜单已导出: {}'.format(fpath))


def parse_book_id(inp):
    """从 URL 或纯数字中提取 book_id"""
    inp = str(inp).strip()
    # 先尝试从 URL 参数中提取 book_id
    if 'book_id=' in inp:
        import urllib.parse as _urlparse
        try:
            parsed = _urlparse.parse_qs(inp.split('?', 1)[-1])
            if 'book_id' in parsed:
                return parsed['book_id'][0]
        except Exception:
            pass
    # 从 fanqienovel.com/page/{id} 链接中提取
    if 'fanqienovel.com/page/' in inp:
        return inp.split('/page/')[-1].split('?')[0].split('/')[0]
    # 纯数字
    try:
        return str(int(inp))
    except (ValueError, TypeError):
        return None


# ==================== 书籍详情查看 ====================
def get_book_detail(book_id):
    """从书籍页面获取详细信息，返回字典或None"""
    url = 'https://fanqienovel.com/page/' + str(book_id)
    try:
        response = session.get(url, timeout=config.get('timeout', 10))
    except Exception as e:
        print('请求失败: {}'.format(e))
        return None
    if response.status_code != 200:
        print('请求失败，状态码: {}'.format(response.status_code))
        return None

    text = response.text
    start_marker = 'window.__INITIAL_STATE__='
    start_idx = text.find(start_marker)
    if start_idx == -1:
        return None
    start_idx += len(start_marker)
    depth = 0
    in_string = False
    escape = False
    end_idx = start_idx
    for i in range(start_idx, len(text)):
        c = text[i]
        if escape:
            escape = False
            continue
        if c == '\\':
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                end_idx = i + 1
                break
    try:
        raw = text[start_idx:end_idx]
        raw = raw.replace(':undefined', ':null').replace(',undefined', ',null')
        state = json.loads(raw)
        p = state.get('page', {})
        # 解析分类
        categories = []
        cat_v2 = p.get('categoryV2', '')
        if cat_v2 and isinstance(cat_v2, str):
            try:
                cats = json.loads(cat_v2)
                for c in cats:
                    if isinstance(c, dict) and c.get('Name'):
                        categories.append(c['Name'])
            except (json.JSONDecodeError, TypeError):
                pass
        # 时间格式化
        last_time = ''
        lpt = p.get('lastPublishTime', '')
        if lpt:
            try:
                last_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(lpt)))
            except (ValueError, TypeError):
                last_time = str(lpt)
        return {
            'bookName': p.get('bookName', '未知'),
            'author': p.get('author', '未知'),
            'authorId': p.get('authorId', ''),
            'wordNumber': p.get('wordNumber', 0),
            'readCount': p.get('readCount', 0),
            'chapterTotal': p.get('chapterTotal', 0),
            'creationStatus': p.get('creationStatus', ''),
            'lastChapterTitle': p.get('lastChapterTitle', ''),
            'lastPublishTime': last_time,
            'abstract': p.get('abstract', ''),
            'description': p.get('description', ''),
            'categories': categories,
            'bookId': p.get('bookId', str(book_id)),
        }
    except (json.JSONDecodeError, ValueError):
        return None


def show_book_detail(book_id):
    """显示书籍详情，返回 book_id 或 None"""
    print('\n正在获取书籍信息...')
    detail = get_book_detail(book_id)
    if not detail:
        print('获取书籍信息失败')
        return None

    status_str = '已完结' if detail['creationStatus'] in (0, '0') else '连载中'
    word_count = int(detail['wordNumber'] or 0)
    read_count = int(detail['readCount'] or 0)
    wc_str = '{:.1f}万字'.format(word_count / 10000) if word_count >= 10000 else '{}字'.format(word_count)
    rc_str = '{:.1f}万'.format(read_count / 10000) if read_count >= 10000 else str(read_count)
    cat_str = '、'.join(detail['categories']) if detail['categories'] else '未分类'

    print('\n' + '=' * 50)
    print('《{}》'.format(detail['bookName']))
    print('=' * 50)
    print('  作者：{}'.format(detail['author']))
    print('  状态：{}'.format(status_str))
    print('  分类：{}'.format(cat_str))
    print('  字数：{}'.format(wc_str))
    print('  章节数：{}'.format(detail['chapterTotal']))
    print('  在读人数：{}'.format(rc_str))
    print('  最近更新：{}'.format(detail['lastChapterTitle']))
    print('  更新时间：{}'.format(detail['lastPublishTime']))
    if detail['description']:
        print('  作者简介：{}'.format(detail['description'][:80]))
    if detail['abstract']:
        ab = detail['abstract'][:200]
        if len(detail['abstract']) > 200:
            ab += '...'
        print('\n  作品简介：')
        print('  ' + ab.replace('\n', '\n  '))
    print('=' * 50)

    while True:
        choice = input('\n输入 d 下载该书，输入 b 返回: ').strip().lower()
        if choice == 'd':
            return detail['bookId']
        elif choice == 'b':
            return None
        else:
            print('输入无效')


# ==================== 批量下载 ====================
def batch_download():
    """批量下载多本书"""
    print('\n--- 批量下载 ---')
    print('请输入书籍 ID 或链接，每行一个（输入空行结束）:')
    book_ids = []
    while True:
        line = input().strip()
        if not line:
            break
        bid = parse_book_id(line)
        if bid:
            book_ids.append(bid)
        else:
            print('  无法识别: {}'.format(line))

    if not book_ids:
        print('未输入任何有效书籍 ID')
        return

    print('\n共 {} 本书待下载:'.format(len(book_ids)))
    for i, bid in enumerate(book_ids):
        print('  {}. ID: {}'.format(i + 1, bid))

    confirm = input('\n确认下载? (y/n): ').strip().lower()
    if confirm != 'y':
        print('已取消')
        return

    success = 0
    fail = 0
    for i, bid in enumerate(book_ids):
        print('\n[{}/{}] 正在下载 ID: {} ...'.format(i + 1, len(book_ids), bid))
        status = down_book(bid)
        if status == 'err':
            print('  下载失败')
            fail += 1
        else:
            success += 1
        if i < len(book_ids) - 1:
            wait = input('  继续下载下一本? (y=继续/n=停止，默认y): ').strip().lower()
            if wait == 'n':
                print('  已停止批量下载')
                break

    print('\n批量下载完成: 成功 {} 本, 失败 {} 本'.format(success, fail))


# ==================== 章节范围下载 ====================
def download_chapter_range(book_id, start_ch, end_ch):
    """下载指定章节范围，保存为TXT"""
    name, chapters, zt = down_zj(book_id)
    if name == 'err':
        print('获取书籍信息失败')
        return 'err'

    chapter_list = list(chapters.items())
    total = len(chapter_list)
    start = max(1, start_ch)
    end = min(total, end_ch)
    if start > end:
        print('章节范围无效')
        return 'err'

    selected = chapter_list[start - 1:end]
    print('\n《{}》共{}章，下载第{}-{}章（共{}章）'.format(name, total, start, end, len(selected)))

    # 断点续传
    safe_name = sanitize_filename(name + '_{}-{}'.format(start, end))
    book_json_path = os.path.join(bookstore_dir, safe_name + '.json')
    cached = {}
    if os.path.exists(book_json_path):
        with open(book_json_path, 'r', encoding='UTF-8') as f:
            cached = json.load(f)

    import concurrent.futures
    results = {}
    results_lock = __import__('threading').Lock()
    save_counter = [0]

    def download_one(title, cid):
        if title in cached:
            cv = cached[title]
            if isinstance(cv, str) and len(cv) > 50:
                return title, cv
        content, ok = down_text(cid)
        time.sleep(random.randint(config['delay'][0], config['delay'][1]) / 1000)
        if ok:
            with results_lock:
                cached[title] = content
                save_counter[0] += 1
                if save_counter[0] >= 5:
                    save_counter[0] = 0
                    with open(book_json_path, 'w', encoding='UTF-8') as f:
                        json.dump(cached, f, ensure_ascii=False)
            return title, content
        return title, ''

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=config.get('xc', 1))
    futures = [executor.submit(download_one, t, c) for t, c in selected]
    pbar = tqdm(total=len(selected), desc='下载进度', unit='章',
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}, {remaining}]')
    for future in concurrent.futures.as_completed(futures):
        title, content = future.result()
        results[title] = content
        pbar.set_postfix_str(title[:20])
        pbar.update(1)
    pbar.close()
    executor.shutdown(wait=True)

    with open(book_json_path, 'w', encoding='UTF-8') as f:
        json.dump(cached, f, ensure_ascii=False)

    # 写入TXT
    fg = '\n' + config['kgf'] * config['kg']
    save_path = config['save_path'] if config['save_path'] else script_dir
    if save_path and not os.path.exists(save_path):
        try:
            os.makedirs(save_path, exist_ok=True)
        except Exception:
            save_path = script_dir
    txt_path = os.path.join(save_path, safe_name + '.txt')
    with open(txt_path, 'w', encoding='UTF-8') as f:
        f.write('小说名：{}\n章节范围：第{}章-第{}章\n\n'.format(name, start, end))
        for title, _ in selected:
            content = cached.get(title, '')
            f.write('\n' + title + fg)
            f.write(content.replace('\n', fg) + '\n' if config['kg'] else content + '\n')
    print('\n保存完成: {}'.format(txt_path))

    # 记录
    try:
        with open(record_path, 'r', encoding='UTF-8') as f:
            records = json.load(f)
        entry = {'book_id': str(book_id), 'name': name, 'time': time.strftime('%Y-%m-%d %H:%M')}
        if entry not in records:
            records.append(entry)
        with open(record_path, 'w', encoding='UTF-8') as f:
            json.dump(records, f, ensure_ascii=False)
    except Exception:
        pass
    return 's'


# ==================== 章节字数统计 ====================
def chapter_stats(book_id):
    """统计已下载书籍的章节字数"""
    name, chapters, zt = down_zj(book_id)
    if name == 'err':
        print('获取书籍信息失败')
        return

    safe_name = sanitize_filename(name)
    book_json_path = os.path.join(bookstore_dir, safe_name + '.json')

    # 如果全本缓存不存在，尝试找范围下载的缓存
    if not os.path.exists(book_json_path):
        found = False
        if os.path.exists(bookstore_dir):
            for fname in os.listdir(bookstore_dir):
                if fname.startswith(safe_name) and fname.endswith('.json'):
                    book_json_path = os.path.join(bookstore_dir, fname)
                    found = True
                    break
        if not found:
            print('《{}》尚未下载，无法统计。请先下载该书。'.format(name))
            return

    with open(book_json_path, 'r', encoding='UTF-8') as f:
        cached = json.load(f)

    chapter_list = list(chapters.keys())
    stats = []
    for title in chapter_list:
        content = cached.get(title, '')
        wc = len(content)
        if wc > 0:
            stats.append((title, wc))

    if not stats:
        print('没有已下载的章节数据')
        return

    word_counts = [s[1] for s in stats]
    total_wc = sum(word_counts)
    avg_wc = total_wc // len(word_counts)
    max_ch = max(stats, key=lambda x: x[1])
    min_ch = min(stats, key=lambda x: x[1])

    # 字数分布
    brackets = [(0, 1000, '<1000'), (1000, 2000, '1000-2000'),
                (2000, 3000, '2000-3000'), (3000, 5000, '3000-5000'),
                (5000, 99999, '>5000')]
    distribution = {}
    for lo, hi, label in brackets:
        count = sum(1 for w in word_counts if lo <= w < hi)
        if count > 0:
            distribution[label] = count

    print('\n' + '=' * 50)
    print('《{}》章节字数统计'.format(name))
    print('=' * 50)
    print('  总章节: {}  已下载: {}'.format(len(chapter_list), len(stats)))
    print('  总字数: {} ({:.1f}万字)'.format(total_wc, total_wc / 10000))
    print('  平均每章: {}字'.format(avg_wc))
    print('  最长章节: 《{}》 {}字'.format(max_ch[0][:20], max_ch[1]))
    print('  最短章节: 《{}》 {}字'.format(min_ch[0][:20], min_ch[1]))
    print('\n  字数分布:')
    for label, count in distribution.items():
        bar = '#' * (count * 30 // len(stats))
        print('    {:12s}: {:3d}章 {}'.format(label, count, bar))
    print('=' * 50)

    # 导出统计
    choice = input('\n导出统计到CSV? (y/n): ').strip().lower()
    if choice == 'y':
        save_path = config['save_path'] if config['save_path'] else script_dir
        if save_path and not os.path.exists(save_path):
            try:
                os.makedirs(save_path, exist_ok=True)
            except Exception:
                save_path = script_dir
        csv_path = os.path.join(save_path, safe_name + '_统计.csv')
        with open(csv_path, 'w', encoding='UTF-8-sig') as f:
            f.write('序号,章节标题,字数\n')
            for i, (title, wc) in enumerate(stats):
                title_clean = title.replace(',', '，').replace('"', '')
                f.write('{},{},{}\n'.format(i + 1, title_clean, wc))
        print('统计已导出: {}'.format(csv_path))


# ==================== 开篇分析 ====================
def opening_analysis():
    """批量提取榜单书籍的开篇正文"""
    print('\n--- 开篇分析 ---')
    print('先选择一个榜单获取书籍列表')
    book_id = None
    # 直接使用榜单功能获取列表
    print('1. 男频')
    print('2. 女频')
    ch = input('选择频道 (1/2): ').strip()
    if ch == '1':
        gender, gender_name, cats = 1, '男频', RANK_CATEGORIES['male']
    elif ch == '2':
        gender, gender_name, cats = 0, '女频', RANK_CATEGORIES['female']
    else:
        print('输入无效')
        return

    print('\n{}阅读榜 分类:'.format(gender_name))
    for i, (cid, cname) in enumerate(cats):
        print('  {:2d}. {}'.format(i + 1, cname))
    cc = input('\n选择分类序号 (1-{}): '.format(len(cats))).strip()
    try:
        idx = int(cc) - 1
        if idx < 0 or idx >= len(cats):
            return
    except ValueError:
        return
    category_id, category_name = cats[idx]

    print('\n正在获取「{}阅读榜·{}」...'.format(gender_name, category_name))
    books = fetch_rank(gender, category_id, rank_type=0, limit=100)
    if not books:
        print('获取榜单失败')
        return

    print('共{}本，显示前10本:'.format(len(books)))
    for i, b in enumerate(books[:10]):
        print('  {:2d}. 《{}》 {}'.format(i + 1, b.get('bookName', '')[:20], b.get('author', '')))

    num = input('\n分析前几本的开篇? (1-10，默认5): ').strip() or '5'
    try:
        num = min(max(int(num), 1), 10)
    except ValueError:
        num = 5

    print('\n提取前{}本的第1章正文...\n'.format(num))
    save_path = config['save_path'] if config['save_path'] else script_dir
    if save_path and not os.path.exists(save_path):
        try:
            os.makedirs(save_path, exist_ok=True)
        except Exception:
            save_path = script_dir
    out_path = os.path.join(save_path, '开篇分析_{}{}.txt'.format(gender_name, category_name))

    with open(out_path, 'w', encoding='UTF-8') as f:
        f.write('番茄小说开篇分析 - {}阅读榜·{}\n'.format(gender_name, category_name))
        f.write('分析时间: {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
        f.write('=' * 60 + '\n\n')

        for i in range(min(num, len(books))):
            b = books[i]
            bid = b.get('bookId', '')
            bname = b.get('bookName', '')
            author = b.get('author', '')
            print('[{}/{}] 《{}》'.format(i + 1, num, bname))
            f.write('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
            f.write('第{}名 《{}》 作者：{}\n'.format(i + 1, bname, author))
            f.write('字数：{}  在读：{}\n'.format(b.get('wordNumber', ''), b.get('read_count', '')))
            f.write('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n')

            # 获取章节列表
            _, chapters, _ = down_zj(bid)
            if not chapters:
                f.write('（获取章节失败）\n\n')
                continue
            first_title = list(chapters.keys())[0]
            first_cid = chapters[first_title]
            content, ok = down_text(first_cid)
            if ok:
                # 限制长度
                if len(content) > 3000:
                    content = content[:3000] + '\n...(后续内容省略)'
                f.write('【{}】\n\n'.format(first_title))
                f.write(content + '\n\n')
            else:
                f.write('（下载失败）\n\n')
            time.sleep(0.5)

    print('\n开篇分析已保存: {}'.format(out_path))


# ==================== 追更更新检测 ====================
def check_updates():
    """检查已下载书籍的更新"""
    if not os.path.exists(record_path):
        print('没有下载记录')
        return

    try:
        with open(record_path, 'r', encoding='UTF-8') as f:
            records = json.load(f)
    except Exception:
        print('读取记录失败')
        return

    if not records:
        print('没有下载记录')
        return

    print('\n--- 追更更新检测 ---')
    updated_books = []

    for i, rec in enumerate(records):
        # 兼容旧格式（纯ID字符串）和新格式（字典）
        if isinstance(rec, str):
            bid = rec
            local_name = '未知'
        elif isinstance(rec, dict):
            bid = rec.get('book_id', '')
            local_name = rec.get('name', '未知')
        else:
            continue

        if not bid:
            continue

        print('[{}/{}] 检查《{}》...'.format(i + 1, len(records), local_name))
        name, chapters, zt = down_zj(bid)
        if name == 'err' or not chapters:
            print('  获取失败，跳过')
            continue

        safe_name = sanitize_filename(name)
        book_json_path = os.path.join(bookstore_dir, safe_name + '.json')
        cached_count = 0
        if os.path.exists(book_json_path):
            with open(book_json_path, 'r', encoding='UTF-8') as f:
                cached = json.load(f)
            cached_count = len(cached)

        online_count = len(chapters)
        new_count = online_count - cached_count

        status_str = '已完结' if zt and '完' in (zt[0] if zt else '') else '连载中'
        if new_count > 0:
            print('  《{}》 {} -> {} (新增{}章) [{}]'.format(
                name, cached_count, online_count, new_count, status_str))
            updated_books.append((bid, name, cached_count, online_count, new_count))
        else:
            print('  《{}》 {} (已是最新) [{}]'.format(name, online_count, status_str))
        time.sleep(0.3)

    print('\n=== 更新汇总 ===')
    if updated_books:
        print('有更新的书籍 {} 本:'.format(len(updated_books)))
        for bid, name, old, new, diff in updated_books:
            print('  《{}》 {} -> {} (+{})'.format(name, old, new, diff))
        choice = input('\n输入序号下载更新 (1-{})，输入 a 全部更新，输入 b 返回: '.format(len(updated_books))).strip()
        if choice.lower() == 'a':
            for bid, name, _, _, _ in updated_books:
                print('\n更新《{}》...'.format(name))
                down_book(bid)
        elif choice.isdigit() and 1 <= int(choice) <= len(updated_books):
            bid = updated_books[int(choice) - 1][0]
            down_book(bid)
    else:
        print('所有书籍都是最新，无需更新')


# ==================== 下载记录管理 ====================
def show_records():
    """查看下载记录"""
    if not os.path.exists(record_path):
        print('没有下载记录')
        return

    try:
        with open(record_path, 'r', encoding='UTF-8') as f:
            records = json.load(f)
    except Exception:
        print('读取记录失败')
        return

    if not records:
        print('没有下载记录')
        return

    print('\n--- 下载记录 (共{}条) ---'.format(len(records)))
    for i, rec in enumerate(records):
        if isinstance(rec, str):
            print('  {}. ID:{}'.format(i + 1, rec))
        elif isinstance(rec, dict):
            t = rec.get('time', '')
            print('  {}. 《{}》 ID:{}  {}'.format(i + 1, rec.get('name', '?'), rec.get('book_id', ''), t))
        else:
            print('  {}. {}'.format(i + 1, rec))

    while True:
        choice = input('\n输入序号重新下载，输入 u 检查更新，输入 c 清空记录，输入 b 返回: ').strip()
        if choice.lower() == 'b':
            return
        elif choice.lower() == 'u':
            check_updates()
            return
        elif choice.lower() == 'c':
            confirm = input('确认清空所有记录? (y/n): ').strip().lower()
            if confirm == 'y':
                with open(record_path, 'w', encoding='UTF-8') as f:
                    json.dump([], f)
                print('记录已清空')
            return
        elif choice.isdigit() and 1 <= int(choice) <= len(records):
            rec = records[int(choice) - 1]
            bid = rec if isinstance(rec, str) else rec.get('book_id', '')
            if bid:
                down_book(bid)
            return
        else:
            print('输入无效')


# ==================== 缓存清理 ====================
def clean_cache():
    """清理已下载书籍的JSON缓存"""
    if not os.path.exists(bookstore_dir):
        print('缓存目录不存在')
        return

    files = [f for f in os.listdir(bookstore_dir) if f.endswith('.json')]
    if not files:
        print('没有缓存文件')
        return

    total_size = 0
    print('\n--- 缓存清理 ---')
    for i, fname in enumerate(files):
        fpath = os.path.join(bookstore_dir, fname)
        size = os.path.getsize(fpath)
        total_size += size
        size_str = '{:.1f}KB'.format(size / 1024) if size < 1024 * 1024 else '{:.1f}MB'.format(size / 1024 / 1024)
        print('  {}. {} ({})'.format(i + 1, fname, size_str))

    size_str = '{:.1f}KB'.format(total_size / 1024) if total_size < 1024 * 1024 else '{:.1f}MB'.format(total_size / 1024 / 1024)
    print('\n共{}个文件，总大小{}'.format(len(files), size_str))
    choice = input('\n1.清理已完结书籍缓存  2.清理全部缓存  3.按序号删除  b返回: ').strip()
    if choice == '1':
        deleted = 0
        for fname in files:
            fpath = os.path.join(bookstore_dir, fname)
            # 简单判断：缓存大小>100KB的可能是已完结全书
            if os.path.getsize(fpath) > 100000:
                os.remove(fpath)
                deleted += 1
                print('  已删除: {}'.format(fname))
        print('清理完成，删除{}个文件'.format(deleted))
    elif choice == '2':
        confirm = input('确认删除全部缓存? (y/n): ').strip().lower()
        if confirm == 'y':
            for fname in files:
                os.remove(os.path.join(bookstore_dir, fname))
            print('已清空全部缓存')
    elif choice == '3':
        idx = input('输入序号: ').strip()
        if idx.isdigit() and 1 <= int(idx) <= len(files):
            os.remove(os.path.join(bookstore_dir, files[int(idx) - 1]))
            print('已删除: {}'.format(files[int(idx) - 1]))


# ==================== CSV榜单导出 ====================
def export_rank_csv(title, books):
    """将榜单数据导出为CSV（含字数、在读、状态等）"""
    save_path = config['save_path'] if config['save_path'] else script_dir
    if save_path and not os.path.exists(save_path):
        try:
            os.makedirs(save_path, exist_ok=True)
        except Exception:
            save_path = script_dir
    safe_title = sanitize_filename(title)
    csv_path = os.path.join(save_path, safe_title + '.csv')
    with open(csv_path, 'w', encoding='UTF-8-sig') as f:
        f.write('排名,书名,作者,字数,在读人数,状态,书籍ID\n')
        for b in books:
            pos = b.get('currentPos', '')
            name = b.get('bookName', '').replace(',', '，').replace('"', '')
            author = b.get('author', '').replace(',', '，')
            wc = b.get('wordNumber', '0')
            rc = b.get('read_count', '0')
            status = '已完结' if b.get('creationStatus') == '0' else '连载中'
            bid = b.get('bookId', '')
            f.write('{},{},{},{},{},{},{}\n'.format(pos, name, author, wc, rc, status, bid))
    print('CSV已导出: {}'.format(csv_path))


# ==================== 工具菜单 ====================
def tools_menu():
    """工具箱菜单"""
    while True:
        print('\n--- 工具箱 ---')
        print('1. 章节范围下载')
        print('2. 章节字数统计')
        print('3. 开篇分析')
        print('4. 追更更新检测')
        print('5. 下载记录管理')
        print('6. 缓存清理')
        print('b. 返回')
        choice = input('选择功能: ').strip()
        if choice == 'b':
            return
        elif choice == '1':
            inp = input('请输入书籍 ID 或链接: ').strip()
            bid = parse_book_id(inp)
            if not bid:
                print('无法识别')
                continue
            name, chapters, _ = down_zj(bid)
            if name == 'err':
                print('获取失败')
                continue
            print('《{}》共{}章'.format(name, len(chapters)))
            rng = input('输入章节范围 (如: 1-10): ').strip()
            try:
                parts = rng.split('-')
                start_ch = int(parts[0])
                end_ch = int(parts[1]) if len(parts) > 1 else start_ch
                download_chapter_range(bid, start_ch, end_ch)
            except (ValueError, IndexError):
                print('格式无效，请如 1-10 输入')
        elif choice == '2':
            inp = input('请输入书籍 ID 或链接: ').strip()
            bid = parse_book_id(inp)
            if bid:
                chapter_stats(bid)
        elif choice == '3':
            opening_analysis()
        elif choice == '4':
            check_updates()
        elif choice == '5':
            show_records()
        elif choice == '6':
            clean_cache()
        else:
            print('输入无效')


# ==================== 主程序 ====================
def main():
    # 命令行参数模式：支持非交互式调用
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        if args[0] == '--book_id' and len(args) >= 2:
            book_id = args[1]
            if len(args) >= 3 and args[2] == '--book_name' and len(args) >= 4:
                pass  # book_name 只用于显示
            status = down_book(book_id)
            if status == 'err':
                print('下载失败，请检查书籍 ID 是否正确')
                sys.exit(1)
            sys.exit(0)
        elif args[0] == '--check' and len(args) >= 2:
            book_id = args[1]
            detail = get_book_detail(book_id)
            if detail:
                import json
                print(json.dumps(detail, ensure_ascii=False))
            else:
                print('获取失败')
                sys.exit(1)
            sys.exit(0)
        elif args[0] == '--search' and len(args) >= 2:
            keyword = args[1]
            # 非交互搜索：直接输出 JSON
            try:
                import urllib.parse as _urlparse
                from abogus import ABogus, BrowserFingerprintGenerator
                params_dict = {
                    'filter': '127,127,127,127',
                    'page_count': '10',
                    'page_index': '0',
                    'query_type': '0',
                    'query_word': keyword,
                }
                query_string = _urlparse.urlencode(params_dict)
                fp = BrowserFingerprintGenerator.generate_fingerprint("Chrome")
                ab = ABogus(user_agent=SEARCH_UA, fp=fp)
                result = ab.generate_abogus(params=query_string, request='GET')
                full_params = result[0]
                url = 'https://fanqienovel.com/api/author/search/search_book/v1?' + full_params
                search_sess = _get_search_session()
                response = search_sess.get(url, timeout=config.get('timeout', 10))
                if response.status_code == 200 and response.text:
                    data = response.json()
                    if data.get('code') == 0:
                        books = data.get('data', {}).get('search_book_data_list', [])
                        results = []
                        for book in books:
                            book_name = str_interpreter(str_interpreter(book.get('book_name', '未知'), 0), 1)
                            author = str_interpreter(str_interpreter(book.get('author', '未知'), 0), 1)
                            results.append({
                                'book_name': book_name,
                                'author': author,
                                'book_id': book.get('book_id', ''),
                                'word_count': book.get('word_count', 0),
                            })
                        import json
                        print(json.dumps(results, ensure_ascii=False, indent=2))
                        sys.exit(0)
                print('搜索失败')
                sys.exit(1)
            except Exception as e:
                print('搜索出错: {}'.format(e))
                sys.exit(1)
        else:
            print('用法: python3 fanqie_txt.py --book_id <id> [--book_name <name>]')
            print('      python3 fanqie_txt.py --check <book_id>')
            print('      python3 fanqie_txt.py --search <keyword>')
            sys.exit(1)

    # 交互式菜单模式
    print()
    print('╔' + '═' * 48 + '╗')
    print('║' + '  🍅 番茄小说下载器 v3.0  @小哲'.ljust(46) + '║')
    print('╠' + '═' * 48 + '╣')
    save_path_display = config.get('save_path', '未设置')
    if len(save_path_display) > 40:
        save_path_display = '...' + save_path_display[-37:]
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
    print('╚' + '═' * 48 + '╝')
    print()

    while True:
        inp = input('\n请输入: ').strip()
        if not inp:
            continue
        if inp.lower() == 'q':
            print('再见！')
            break
        if inp.lower() == 'ss':
            book_id = search_book()
            if book_id:
                print('书籍 ID: {}'.format(book_id))
                status = down_book(book_id)
                if status == 'err':
                    print('下载失败，请检查书籍 ID 是否正确')
            continue
        if inp.lower() == 'ph':
            book_id = show_rank()
            if book_id:
                print('书籍 ID: {}'.format(book_id))
                status = down_book(book_id)
                if status == 'err':
                    print('下载失败，请检查书籍 ID 是否正确')
            continue
        if inp.lower() == 'vd':
            inp2 = input('请输入书籍 ID 或链接: ').strip()
            bid = parse_book_id(inp2)
            if bid:
                book_id = show_book_detail(bid)
                if book_id:
                    print('书籍 ID: {}'.format(book_id))
                    status = down_book(book_id)
                    if status == 'err':
                        print('下载失败，请检查书籍 ID 是否正确')
            else:
                print('无法识别书籍 ID')
            continue
        if inp.lower() == 'bd':
            batch_download()
            continue
        if inp.lower() == 't':
            tools_menu()
            continue
        if inp.lower() == 's':
            inp = input('选择 (1-4, b返回): ').strip()
            if inp == '1':
                try:
                    v = int(input('缩进空格数 (0-8): '))
                    config['kg'] = max(0, min(8, v))
                except: pass
            elif inp == '2':
                config.select_save_path()
            elif inp == '3':
                config['save_mode'] = 2 if config['save_mode'] == 1 else 1
                print('下载模式已切换为:', '单个TXT' if config['save_mode'] == 1 else '分章TXT')
            elif inp == '4':
                try:
                    v = int(input('线程数 (1-5): '))
                    config['xc'] = max(1, min(5, v))
                except: pass
            continue
            print('2. 保存路径 (当前: {})'.format(config.get('save_path', '未设置')))
            print('3. 下载模式 (当前: {})'.format('单个TXT' if config['save_mode'] == 1 else '分章TXT'))
            print('4. 线程数 (当前: {})'.format(config['xc']))
            print('2. 段首占位符 (当前: "{}")'.format(config['kgf']))
            print('3. 下载延迟范围ms (当前: {}~{})'.format(config['delay'][0], config['delay'][1]))
            sm = '单个TXT' if config['save_mode'] == 1 else '分章TXT'
            print('4. 保存方式 (当前: {})'.format(sm))
            print('5. 下载线程数 (当前: {})'.format(config['xc']))
            sp = config.get('save_path') or script_dir
            print(f'6. 保存路径 (当前: {sp})')
            cn = '开' if config.get('enable_chapter_numbering') else '关'
            print(f'7. 章节编号 (当前: {cn})')
            choice = input('选择设置项 (1-7): ').strip()
            if choice == '1':
                config['kg'] = int(input('缩进空格数 (当前{}): '.format(config['kg'])) or config['kg'])
            elif choice == '2':
                v = input('占位符 (当前"{}", 直接回车不改): '.format(config['kgf']))
                if v: config['kgf'] = v
            elif choice == '3':
                config['delay'][0] = int(input('延迟下限ms (当前{}): '.format(config['delay'][0])) or config['delay'][0])
                config['delay'][1] = int(input('延迟上限ms (当前{}): '.format(config['delay'][1])) or config['delay'][1])
            elif choice == '4':
                m = input('1=单个TXT  2=分章TXT: ').strip()
                if m in ('1', '2'):
                    config['save_mode'] = int(m)
            elif choice == '5':
                config['xc'] = int(input('线程数 (当前{}): '.format(config['xc'])) or config['xc'])
            elif choice == '6':
                sp_now = config.get('save_path') or script_dir
                p = input('保存路径 (当前: {}, 直接回车不改): '.format(sp_now)).strip()
                if p:
                    config['save_path'] = p
            elif choice == '7':
                config['enable_chapter_numbering'] = input('开启章节编号? (1=开/2=关): ').strip() == '1'
            print('设置已保存')
            continue

        # 尝试下载
        book_id = parse_book_id(inp)
        if not book_id:
            print('无法识别书籍 ID，请检查输入')
            continue
        print(f'书籍 ID: {book_id}')
        status = down_book(book_id)
        if status == 'err':
            print('下载失败，请检查书籍 ID 是否正确')


if __name__ == '__main__':
    main()

"""Build Simplified Chinese and English homepages from index.html.
Translations are keyed by the original Traditional Chinese text. Add translations
for new copy to home-translations.json before rebuilding. No third-party packages.
Run: python3 tools/build_home_languages.py
"""
import html
import json
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
class CopyReader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.values = set()
    def add(self, value):
        if re.search(r'[\u4e00-\u9fff]', value):
            self.values.add(value.strip())
    def handle_data(self, value):
        self.add(value)
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('alt', 'aria-label', 'title', 'placeholder') or (tag == 'meta' and key == 'content'):
                self.add(value or '')

def language_nav(lang):
    labels = [('zh-Hant', 'index.html', '繁體'), ('zh-Hans', 'index-sc.html', '简体'), ('en', 'index-en.html', 'English')]
    name = {'zh-Hant': '語言切換', 'zh-Hans': '语言切换', 'en': 'Choose language'}[lang]
    links = []
    for code, target, label in labels:
        current = ' aria-current="page"' if code == lang else ''
        links.append(f'<a href="{target}" lang="{code}" hreflang="{code}"{current}>{label}</a>')
    return f'<nav class="language-switch" aria-label="{name}">\n      '+ '\n      <span aria-hidden="true">/</span>\n      '.join(links)+'\n    </nav>'

source = (ROOT / 'index.html').read_text()
# Replace the switch after translating, so language names always stay native.
source = re.sub(r'<nav class="language-switch".*?</nav>', '<!-- LANGUAGE_SWITCH -->', source, count=1, flags=re.S)
source = re.sub(r'\s*<link [^>]*hreflang="(?:zh-Hant|zh-Hans|en)"[^>]*>', '', source)
source = source.replace('</head>', '    <link rel="alternate" hreflang="zh-Hant" href="index.html">\n    <link rel="alternate" hreflang="zh-Hans" href="index-sc.html">\n    <link rel="alternate" hreflang="en" href="index-en.html">\n</head>')
source = source.replace('script.js?v=20261010', 'script.js?v=languages-20261031').replace('home.css?v=teaching-practice-20261031', 'home.css?v=languages-20261031')
reader = CopyReader(); reader.feed(source)
translations = json.loads((ROOT / 'tools/home-translations.json').read_text())
for lang, filename in [('zh-Hans', 'index-sc.html'), ('en', 'index-en.html')]:
    mapping = translations[lang]
    missing = reader.values - mapping.keys()
    if missing:
        raise ValueError(f'Missing {lang} translations: {sorted(missing)}')
    def text(value):
        key = html.unescape(value.strip())
        if key not in mapping:
            return value
        prefix = value[:len(value)-len(value.lstrip())]
        suffix = value[len(value.rstrip()):]
        return prefix + html.escape(mapping[key], quote=False) + suffix
    def attribute(match):
        key = html.unescape(match[3])
        value = html.escape(mapping.get(key, key), quote=True)
        return match[1] + match[2] + value + match[2]
    pieces = re.split(r'(<[^>]*>)', source)
    for i, piece in enumerate(pieces):
        if piece.startswith('<'):
            pieces[i] = re.sub(r'((?:alt|aria-label|title|placeholder|content)\s*=\s*)([\"\x27])(.*?)\2', attribute, piece)
        else:
            pieces[i] = text(piece)
    result = ''.join(pieces).replace('lang="zh-Hant"', f'lang="{lang}"', 1)
    result = result.replace('<!-- LANGUAGE_SWITCH -->', language_nav(lang))
    if lang == 'zh-Hans':
        result = result.replace('+TC:', '+SC:')
        for target in ['proposal', 'hooked-workshop', 'hooked-outline']:
            result = result.replace(f'href="{target}.html', f'href="{target}-sc.html')
    else:
        result = re.sub(r'<h1>.*?</h1>', '<h1>Think clearly.<br>Speak with purpose.<br>Collaborate in the age of AI.</h1>', result, count=1, flags=re.S)
        result = result.replace('episodes of Learning<br>Podcast', 'episodes of<br>Learning Without Boundaries')
        result = result.replace('weeks of ARC<br>Parent Circle', 'weeks of<br>ARC Parent Circle')
        result = result.replace('。</video>', '.</video>').replace('</a>。', '</a>.')
    (ROOT / filename).write_text(result)
(ROOT / 'index.html').write_text(source.replace('<!-- LANGUAGE_SWITCH -->', language_nav('zh-Hant')))
print('Built index-sc.html and index-en.html; updated homepage language links.')

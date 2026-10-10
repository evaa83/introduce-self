"""Generate static Simplified Chinese pages.
Run: python3 -m pip install opencc-python-reimplemented==0.1.7 beautifulsoup4==4.12.3
     python3 tools/build_simplified.py
Only display text is converted; asset paths, IDs, scripts and external URLs stay intact.
"""
from pathlib import Path
from bs4 import BeautifulSoup, Comment, Doctype
from opencc import OpenCC

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index', 'proposal', 'hooked-workshop', 'hooked-outline']
convert = OpenCC('t2s').convert
for page in PAGES:
    soup = BeautifulSoup((ROOT / f'{page}.html').read_text(), 'html.parser')
    for node in list(soup.find_all(string=True)):
        if isinstance(node, (Comment, Doctype)) or node.parent.name in ('script', 'style'):
            continue
        if node.find_parent(class_='language-switch'):
            continue
        node.replace_with(convert(str(node)))
    for tag in soup.find_all(True):
        for attr in ('alt', 'title', 'aria-label', 'placeholder'):
            if attr in tag.attrs:
                tag[attr] = convert(tag[attr])
        if tag.name == 'meta' and tag.get('name') == 'description':
            tag['content'] = convert(tag['content'])
        if tag.name == 'a' and not tag.find_parent(class_='language-switch'):
            href = tag.get('href', '')
            for target in PAGES:
                if href == f'{target}.html' or href.startswith(f'{target}.html#'):
                    tag['href'] = href.replace(f'{target}.html', f'{target}-sc.html', 1)
                    break
        if tag.name == 'link' and 'fonts.googleapis.com' in tag.get('href', ''):
            tag['href'] = tag['href'].replace('+TC:', '+SC:')
    # Convert font-family names in inline workshop styles only, never URLs.
    for style in soup.find_all('style'):
        style.string = str(style.string).replace('Noto Sans TC', 'Noto Sans SC').replace('Noto Serif TC', 'Noto Serif SC')
    soup.html['lang'] = 'zh-Hans'
    for link in soup.select('.language-switch a'):
        link.attrs.pop('aria-current', None)
        if link.get('lang') == 'zh-Hans':
            link['aria-current'] = 'page'
    (ROOT / f'{page}-sc.html').write_text(str(soup))

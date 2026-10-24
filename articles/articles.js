(() => {
  'use strict';
  const list = document.querySelector('[data-article-list]');
  if (!list) return;
  const root = new URL(list.dataset.root || './', document.baseURI);
  const status = document.querySelector('#article-status');
  const search = document.querySelector('#article-search');
  const category = document.querySelector('#article-category');
  const element = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text) node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  const safePath = value => typeof value === 'string' && !value.includes('..') && /^(?:\d+\/|assets\/\d+\/[a-zA-Z0-9_-]+\.(?:jpg|jpeg|png|webp|gif))$/.test(value);
  async function load() {
    try {
      const response = await fetch(new URL(list.dataset.manifest, document.baseURI), { cache: 'no-cache' });
      if (!response.ok) throw new Error('Article list unavailable');
      const manifest = await response.json();
      if (manifest.version !== 1 || !Array.isArray(manifest.articles)) throw new Error('Invalid article list');
      const articles = manifest.articles.filter(a => Number.isSafeInteger(a.episodeNumber) && safePath(a.url) && typeof a.title === 'string' && Array.isArray(a.categories) && Array.isArray(a.tags));
      if (category) {
        [...new Set(articles.flatMap(a => a.categories))].sort().forEach(name => {
          const option = element('option', name); option.value = name; category.append(option);
        });
      }
      function render() {
        const query = (search?.value || '').trim().toLocaleLowerCase();
        const selected = category?.value || '';
        let filtered = articles.filter(a => (!selected || a.categories.includes(selected)) && [a.title, a.summary, a.episodeNumber, ...a.tags, ...a.categories].join(' ').toLocaleLowerCase().includes(query));
        if (list.dataset.limit) filtered = filtered.slice(0, Number(list.dataset.limit));
        list.replaceChildren();
        filtered.forEach(article => {
          const card = element('article', '', 'article-card');
          const link = element('a', '', 'article-card-link');
          link.href = new URL(article.url, root).href;
          if (article.cover && safePath(article.cover)) {
            const image = element('img'); image.src = new URL(article.cover, root).href; image.alt = article.title; image.loading = 'lazy'; image.width = 800; image.height = 520; link.append(image);
          }
          const body = element('div', '', 'article-card-body');
          body.append(element('p', `第 ${article.episodeNumber} 集${article.categories.length ? ' · ' + article.categories.join('、') : ''}`, 'article-meta'));
          body.append(element('h3', article.title));
          body.append(element('p', article.summary || article.subtitle || '', 'article-excerpt'));
          body.append(element('span', '閱讀全文 →', 'article-read'));
          link.append(body); card.append(link); list.append(card);
        });
        if (status) status.textContent = filtered.length ? `共 ${filtered.length} 篇文章` : articles.length ? '沒有符合條件的文章，請試試其他關鍵字。' : '專題文章整理中，歡迎先收聽無邊界學習 Podcast。';
      }
      search?.addEventListener('input', render);
      category?.addEventListener('change', render);
      render();
    } catch {
      if (status) status.textContent = '文章列表暫時無法載入，請稍後重新整理。';
      else list.append(element('p', '專題文章整理中，歡迎查看全部文章。'));
    }
  }
  void load();
})();

(function () {
  var input = document.getElementById('search-input');
  var results = document.getElementById('search-results');
  if (!input || !results) return;

  var INDEX = null;
  var loadingPromise = null;

  function loadIndex() {
    if (INDEX) return Promise.resolve(INDEX);
    if (loadingPromise) return loadingPromise;
    loadingPromise = fetch('/search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (data) { INDEX = data; return data; });
    return loadingPromise;
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function highlight(text, terms) {
    var escaped = escapeHtml(text);
    terms.forEach(function (t) {
      if (!t) return;
      var re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
      escaped = escaped.replace(re, '<mark>$1</mark>');
    });
    return escaped;
  }

  function search(query) {
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    var scored = [];
    INDEX.forEach(function (item) {
      var hay = (item.t + ' ' + item.s + ' ' + item.c).toLowerCase();
      var score = 0;
      var matched = true;
      terms.forEach(function (t) {
        var titleHits = (item.t.toLowerCase().match(new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length;
        var bodyHits = (hay.match(new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length;
        if (titleHits === 0 && bodyHits === 0) matched = false;
        score += titleHits * 5 + bodyHits;
      });
      if (matched) scored.push({ item: item, score: score });
    });
    scored.sort(function (a, b) { return b.score - a.score; });
    return scored.slice(0, 10).map(function (x) { return x.item; });
  }

  function snippetAround(text, term) {
    var lower = text.toLowerCase();
    var i = lower.indexOf(term.toLowerCase());
    if (i < 0) return text.slice(0, 80);
    var start = Math.max(0, i - 30);
    var end = Math.min(text.length, i + 60);
    return (start > 0 ? '…' : '') + text.slice(start, end) + (end < text.length ? '…' : '');
  }

  function render(items, terms) {
    if (!items.length) {
      results.innerHTML = '<li class="empty">没有匹配结果</li>';
      results.classList.add('show');
      return;
    }
    results.innerHTML = items.map(function (it) {
      var snippet = snippetAround(it.s, terms[0] || '');
      return '<li><a href="' + it.p + '">'
        + '<div class="r-title">' + highlight(it.t, terms) + '</div>'
        + '<div class="r-meta">' + it.d + ' · ' + escapeHtml(it.c) + '</div>'
        + '<div class="r-snip">' + highlight(snippet, terms) + '</div>'
        + '</a></li>';
    }).join('');
    results.classList.add('show');
  }

  function clear() {
    results.innerHTML = '';
    results.classList.remove('show');
  }

  var debounceTimer;
  input.addEventListener('input', function () {
    clearTimeout(debounceTimer);
    var q = input.value.trim();
    if (!q) { clear(); return; }
    debounceTimer = setTimeout(function () {
      loadIndex().then(function () {
        var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
        render(search(q), terms);
      });
    }, 120);
  });

  input.addEventListener('focus', function () {
    if (input.value.trim()) results.classList.add('show');
  });

  document.addEventListener('click', function (e) {
    if (!input.contains(e.target) && !results.contains(e.target)) {
      results.classList.remove('show');
    }
  });

  input.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { input.value = ''; clear(); input.blur(); }
  });
})();

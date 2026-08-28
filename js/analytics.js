/* ============================================================================
   李佳芮博客 DataFinder 埋点层
   - 静态站点专用：无构建、无依赖
   - 事件名沿用官网口径：page_view / button_click
   ========================================================================== */
(function () {
  if (window.LJRAnalytics && window.LJRAnalytics.__installed) return;

  var RAW_CONFIG = window.LJR_ANALYTICS_CONFIG || window.JZ_ANALYTICS_CONFIG || {};
  var SDK_URL = 'https://lf3-data.volccdn.com/obj/data-static/log-sdk/collect/5.0/collect-rangers-v5.2.11.js';
  var CONFIG = {
    appId: String(RAW_CONFIG.app_id || RAW_CONFIG.appId || '20011391'),
    channel: RAW_CONFIG.channel || 'cn',
    channelDomain: RAW_CONFIG.channel_domain || RAW_CONFIG.channelDomain || 'https://gator.volces.com',
    sdkUrl: RAW_CONFIG.sdk_url || RAW_CONFIG.sdkUrl || SDK_URL,
    enabled: RAW_CONFIG.enabled !== false,
    debug: !!RAW_CONFIG.debug || /(?:^|[?&])ljr_analytics_debug=1(?:&|$)/.test(location.search)
  };

  var EVENT_PAGE_VIEW = 'page_view';
  var EVENT_BUTTON_CLICK = 'button_click';
  var started = false;

  var CAT_LABEL = {
    thought: '思考',
    chatbot: 'Chatbot',
    presentation: '演讲',
    interview: '访谈',
    project: '项目',
    reading: '读书',
    saas: 'SaaS',
    microsoft: 'Microsoft',
    tech: 'Tech'
  };

  function merge(a, b) {
    var out = {}, k;
    for (k in a) if (Object.prototype.hasOwnProperty.call(a, k)) out[k] = a[k];
    for (k in b) if (Object.prototype.hasOwnProperty.call(b, k)) out[k] = b[k];
    return out;
  }

  function cleanProps(props) {
    var out = {};
    props = props || {};
    Object.keys(props).forEach(function (key) {
      var value = props[key];
      if (value === undefined || value === null) return;
      if (typeof value === 'string') {
        value = value.trim();
        if (!value) return;
        if (value.length > 1000) value = value.slice(0, 1000);
      } else if (Array.isArray(value)) {
        value = value.join(',');
      } else if (typeof value !== 'number' && typeof value !== 'boolean') {
        value = String(value);
      }
      out[key] = value;
    });
    return out;
  }

  function normalizePath() {
    var path = location.pathname || '/';
    path = path.replace(/\/{2,}/g, '/');
    if (!path) return '/';
    return path;
  }

  function params() {
    var out = {};
    try {
      var sp = new URLSearchParams(location.search);
      ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
        if (sp.has(k)) out[k] = sp.get(k);
      });
    } catch (_) {}
    return out;
  }

  function metaContent(selector) {
    var el = document.querySelector(selector);
    return el ? el.getAttribute('content') || '' : '';
  }

  function attr(selector, name) {
    var el = document.querySelector(selector);
    return el ? el.getAttribute(name) || '' : '';
  }

  function pageTitle() {
    return metaContent('meta[property="og:title"]') ||
      textOf(document.querySelector('h1')) ||
      document.title ||
      '';
  }

  function pageMeta() {
    var path = normalizePath();
    if (path === '/' || path === '/index.html') {
      return { first_menu: '首页', second_menu: '首页', content_type: 'home' };
    }
    if (/^\/blog\/?$/.test(path)) {
      return { first_menu: '博客', second_menu: '全部文章', content_type: 'list' };
    }
    if (/^\/claude\/?$/.test(path)) {
      return { first_menu: 'Claude 永动机', second_menu: 'Claude 永动机', content_type: 'list' };
    }
    if (/^\/slides\/?$/.test(path)) {
      return { first_menu: '分享 PPT', second_menu: '分享 PPT', content_type: 'list' };
    }
    if (/^\/slides\/files\//.test(path)) {
      return { first_menu: '分享 PPT', second_menu: pageTitle(), content_type: 'slides' };
    }
    if (/^\/yearly\/?$/.test(path)) {
      return { first_menu: '年度思考', second_menu: '年度思考', content_type: 'list' };
    }
    if (/^\/about\/?$/.test(path)) {
      return { first_menu: '关于', second_menu: '关于', content_type: 'page' };
    }
    if (/^\/media\/?$/.test(path)) {
      return { first_menu: '关于', second_menu: '媒体报道', content_type: 'page' };
    }
    if (/^\/links\/?$/.test(path)) {
      return { first_menu: '关于', second_menu: '友情链接', content_type: 'page' };
    }
    if (/^\/help\/?$/.test(path)) {
      return { first_menu: '关于', second_menu: '帮助', content_type: 'page' };
    }

    var m = path.match(/^\/([^/]+)\//);
    var cat = m ? m[1] : '';
    if (CAT_LABEL[cat]) {
      return { first_menu: '博客', second_menu: CAT_LABEL[cat], content_type: 'article', category: cat };
    }
    if (/^\/(?:archives|categories|tags|page)\//.test(path)) {
      return { first_menu: '博客', second_menu: '旧链接跳转', content_type: 'redirect' };
    }
    if (path === '/404.html') {
      return { first_menu: '系统页面', second_menu: '404', content_type: 'error' };
    }
    return { first_menu: '其他页面', second_menu: pageTitle() || path, content_type: 'page' };
  }

  function commonProps() {
    var meta = pageMeta();
    return merge({
      app_type: '博客',
      zone: 'Z区',
      first_menu: meta.first_menu,
      second_menu: meta.second_menu
    }, params());
  }

  function articleProps(meta) {
    var tags = [];
    document.querySelectorAll('.post-tag, .slide-tag').forEach(function (tag) {
      var t = textOf(tag).replace(/^#/, '');
      if (t) tags.push(t);
    });
    var category = textOf(document.querySelector('.post-cat')) || CAT_LABEL[meta.category] || (meta.content_type === 'slides' ? '演讲' : '');
    return cleanProps({
      content_type: meta.content_type,
      article_title: pageTitle(),
      article_path: normalizePath(),
      article_category: category,
      article_tags: tags,
      article_date: metaContent('meta[property="article:published_time"]')
    });
  }

  function pageProps() {
    var meta = pageMeta();
    var props = {
      view_type: 'page',
      page_title: document.title || '',
      page_path: normalizePath(),
      content_type: meta.content_type,
      canonical_url: attr('link[rel="canonical"]', 'href')
    };
    if (meta.content_type === 'article' || meta.content_type === 'slides') {
      props = merge(props, articleProps(meta));
    }
    return props;
  }

  function installStub() {
    var exportObj = 'collectEvent';
    window.LogAnalyticsObject = exportObj;
    if (!window[exportObj]) {
      var collect = function () { collect.q.push(arguments); };
      collect.q = collect.q || [];
      window[exportObj] = collect;
    }
    window[exportObj].l = Number(new Date());
  }

  function loadSdk() {
    if (document.querySelector('script[data-ljr-df-sdk]')) return;
    var script = document.createElement('script');
    script.src = CONFIG.sdkUrl;
    script.async = true;
    script.setAttribute('data-ljr-df-sdk', '1');
    (document.head || document.body).appendChild(script);
  }

  function log() {
    if (!CONFIG.debug || !window.console) return;
    console.log.apply(console, arguments);
  }

  function ce() {
    if (!CONFIG.enabled) return;
    if (!window.collectEvent) installStub();
    window.collectEvent.apply(window, arguments);
  }

  function init() {
    if (started) return;
    started = true;
    if (!CONFIG.enabled || !CONFIG.appId || !CONFIG.channelDomain) {
      log('[LJRAnalytics] disabled');
      return;
    }
    installStub();
    ce('init', {
      app_id: /^\d+$/.test(CONFIG.appId) ? Number(CONFIG.appId) : CONFIG.appId,
      channel: CONFIG.channel,
      channel_domain: CONFIG.channelDomain,
      log: CONFIG.debug,
      autotrack: false,
      disable_auto_pv: true
    });
    ce('config', cleanProps({
      app_type: '博客',
      zone: 'Z区',
      site_name: '李佳芮的博客'
    }));
    ce('start');
    loadSdk();
  }

  function track(eventName, props) {
    if (eventName !== EVENT_PAGE_VIEW && eventName !== EVENT_BUTTON_CLICK) {
      log('[LJRAnalytics] ignored unsupported event', eventName);
      return;
    }
    init();
    var payload = cleanProps(merge(commonProps(), props || {}));
    log('[LJRAnalytics]', eventName, payload);
    ce(eventName, payload);
  }

  function trackPage() {
    track(EVENT_PAGE_VIEW, pageProps());
  }

  function textOf(el) {
    return el ? (el.getAttribute('aria-label') || el.textContent || '').replace(/\s+/g, ' ').trim() : '';
  }

  function closest(el, selector) {
    while (el && el !== document) {
      if (el.matches && el.matches(selector)) return el;
      el = el.parentNode;
    }
    return null;
  }

  function targetInfo(href) {
    var info = { target_url: '', target_path: '', target_type: 'action' };
    if (!href) return info;
    try {
      var url = new URL(href, location.href);
      info.target_url = url.href;
      info.target_path = url.pathname + url.search + url.hash;
      if (href.charAt(0) === '#') info.target_type = 'anchor';
      else if (url.hostname !== location.hostname) info.target_type = 'external';
      else if (/\.(?:pdf|pptx?|docx?|xlsx?|zip|mp4|mov)(?:$|\?)/i.test(url.pathname)) info.target_type = 'download';
      else info.target_type = 'internal';
    } catch (_) {
      info.target_url = href;
    }
    return info;
  }

  function areaOf(el) {
    if (closest(el, '.topnav')) return '顶部导航';
    if (closest(el, '.home-cards')) return '首页入口卡片';
    if (closest(el, '.search-results')) return '搜索结果';
    if (closest(el, '.feed')) return '文章列表';
    if (closest(el, '.post-related')) return '相关阅读';
    if (closest(el, '.post-nav')) return '上下篇导航';
    if (closest(el, '.post-content')) return '正文内容';
    if (closest(el, '.sidebar')) return '侧栏';
    if (closest(el, '.site-foot')) return '页脚';
    return '页面链接';
  }

  function bindClickTracking() {
    document.addEventListener('click', function (e) {
      var el = closest(e.target, 'a, button, [role="button"], [data-track-click], [data-track-name]');
      if (!el) return;
      var href = el.getAttribute('href') || '';
      var area = el.getAttribute('data-track-area') || areaOf(el);
      var name = el.getAttribute('data-track-name') || textOf(el) || href || '未命名点击';
      var target = targetInfo(href);
      track(EVENT_BUTTON_CLICK, merge({
        button_name: name,
        button_source: area + '·' + name,
        button_area: area
      }, target));
    }, true);
  }

  function onReady(fn) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  window.LJRAnalytics = {
    __installed: true,
    config: CONFIG,
    track: track,
    trackPage: trackPage
  };

  onReady(function () {
    trackPage();
    bindClickTracking();
  });
})();

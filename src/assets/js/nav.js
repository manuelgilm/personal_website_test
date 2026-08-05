// Shared site navigation (single source of truth).
// Inject into any page by placing <ul id="nav-main"></ul> inside <nav id="navbar">
// and loading this script BEFORE main.js so scroll/active bindings work.
(function () {
  'use strict';

  var target = document.getElementById('nav-main');
  if (!target) return;

  // Page type detection based on the current file name.
  var path = window.location.pathname.split('/').pop() || 'index.html';
  var isHome = path === 'index.html';
  // Link prefix for single-page section links on non-index pages.
  var p = isHome ? '#' : 'index.html#';
  // Which nav item should be highlighted on this page.
  var activeItem = isHome ? (window.location.hash.replace('#', '') || 'hero')
    : (path.indexOf('ai-room') !== -1 ? 'ai-room'
    : (path.indexOf('blog') !== -1 ? 'journal'
    : (path.indexOf('portfolio') !== -1 ? 'portfolio' : '')));

  var items = [
    { id: 'hero',     label: 'Home',
      href: p + 'hero',     scroll: true, visible: true },
    { id: 'about',    label: 'About',
      href: p + 'about',    scroll: true, visible: true },
    { id: 'journal',  label: 'Blog',
      href: p + 'journal',  scroll: true, visible: true },
    { id: 'ai-room',  label: 'AI Room',
      href: 'ai-room.html', scroll: false, visible: true },
    { id: 'youwiki',  label: 'YouWiki', dropdown: true, visible: true },
    { id: 'contact',  label: 'Contact',
      href: p + 'contact',  scroll: true, visible: true }
  ];

  var html = '';
  items.forEach(function (item) {
    if (!item.visible) return;
    if (item.dropdown) {
      var isActive = item.id === activeItem;
      html += '<li class="dropdown' + (isActive ? ' active' : '') + '">' +
        '<a href="#"><span>YouWiki</span> <i class="bi bi-chevron-down"></i></a>' +
        '<ul>' +
        '<li><a href="../docs/site_en/index.html" target="_blank">English</a></li>' +
        '<li><a href="../docs/site_es/index.html" target="_blank">Español</a></li>' +
        '</ul></li>';
    } else {
      var cls = item.id === activeItem ? ' class="nav-link active"' : ' class="nav-link"';
      if (item.scroll) cls = cls.replace('nav-link', 'nav-link scrollto');
      html += '<li><a' + cls + ' href="' + item.href + '">' + item.label + '</a></li>';
    }
  });

  target.innerHTML = html;
})();
---
layout: archive
title: "Notes"
permalink: /notes/
author_profile: true
---

{% include base_path %}
{% assign notes = site.data.notes | sort: "date" | reverse %}
{% assign grouped_notes = notes | group_by: "kind" | sort: "name" %}

<style>
  /* Notes index — Anthropic-inspired palette
     (warm ivory · clay/terracotta accent · neutral kraft secondary · serif display). */
  .notes-index {
    --n-paper: #f0ede4;
    --n-surface: #fdfbf6;
    --n-ink: #1f1d1a;
    --n-muted: #6f6a61;
    --n-soft-ink: #4c473f;
    --n-line: #e4ddcd;
    --n-accent: #c15f3c;
    --n-accent-soft: #f7ece4;
    --n-accent-ink: #974326;
    --n-accent-2: #7c7468;
    --n-accent-2-soft: #f3ede2;
    --n-shadow: 0 16px 40px rgba(31, 37, 40, 0.1);
    --n-radius: 12px;
    --n-serif: "Iowan Old Style", "Palatino", "Songti SC", "Noto Serif CJK SC", Georgia, serif;
    --n-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
    min-width: 0;
    margin: 0;
    padding: clamp(20px, 3.2vw, 34px);
    border: 1px solid var(--n-line);
    border-radius: 18px;
    background:
      linear-gradient(90deg, rgba(193, 95, 60, 0.05) 1px, transparent 1px),
      linear-gradient(180deg, rgba(120, 105, 85, 0.04) 1px, transparent 1px),
      var(--n-paper);
    background-size: 44px 44px;
    color: var(--n-ink);
    font-family: var(--n-sans);
  }

  .notes-index,
  .notes-index * {
    box-sizing: border-box;
  }

  /* hide the default minimal-mistakes page title; replaced by the hero below */
  .archive > .page__title {
    display: none;
  }

  /* ---------- hero ---------- */
  .notes-hero {
    margin: 0 0 1.4rem;
  }

  .notes-hero__kicker {
    margin: 0 0 0.6rem;
    color: var(--n-accent);
    font-family: var(--n-sans);
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }

  .notes-hero__title {
    margin: 0;
    color: var(--n-ink);
    font-family: var(--n-serif);
    font-size: clamp(1.9rem, 4.6vw, 2.9rem);
    font-weight: 700;
    line-height: 1.14;
  }

  .notes-lead {
    max-width: 46rem;
    margin: 0.9rem 0 0;
    color: var(--n-muted);
    font-size: 1rem;
    line-height: 1.75;
  }

  /* ---------- controls panel ---------- */
  .notes-panel {
    margin: 0 0 1.2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--n-line);
  }

  .notes-toolbar {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 0.75rem;
    align-items: center;
    margin-bottom: 0.85rem;
    min-width: 0;
  }

  .notes-count {
    min-width: 0;
    color: var(--n-muted);
    font-size: 0.82rem;
    overflow-wrap: anywhere;
  }

  .notes-count [data-notes-visible-count] {
    color: var(--n-accent);
    font-weight: 700;
    font-variant-numeric: tabular-nums;
  }

  .notes-search {
    box-sizing: border-box;
    width: min(100%, 20rem);
    max-width: 100%;
    min-width: 0;
    min-height: 2.3rem;
    padding: 0.5rem 0.8rem;
    border: 1px solid var(--n-line);
    border-radius: 9px;
    background: var(--n-surface);
    color: var(--n-ink);
    font: inherit;
    font-size: 0.9rem;
  }

  .notes-search::placeholder {
    color: #a79f92;
  }

  .notes-search:focus {
    outline: none;
    border-color: var(--n-accent);
    box-shadow: 0 0 0 3px rgba(193, 95, 60, 0.18);
  }

  .notes-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .notes-filter-button {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    min-height: 2rem;
    padding: 0.32rem 0.74rem;
    border: 1px solid var(--n-line);
    border-radius: 999px;
    background: var(--n-surface);
    color: var(--n-muted);
    cursor: pointer;
    font: inherit;
    font-size: 0.8rem;
    line-height: 1.3;
    transition: color 0.15s ease, border-color 0.15s ease, background 0.15s ease, box-shadow 0.15s ease;
  }

  .notes-filter-button:hover {
    border-color: rgba(193, 95, 60, 0.5);
    color: var(--n-accent);
  }

  .notes-filter-button.is-active {
    border-color: var(--n-accent);
    background: var(--n-accent);
    color: #fff;
    box-shadow: 0 8px 18px rgba(193, 95, 60, 0.24);
  }

  .notes-filter-button__count {
    font-variant-numeric: tabular-nums;
    font-weight: 600;
    opacity: 0.75;
  }

  .notes-sort-note {
    margin: 0.8rem 0 0;
    color: var(--n-muted);
    font-size: 0.78rem;
  }

  /* ---------- list + cards ---------- */
  .notes-list {
    display: grid;
    gap: 0.85rem;
  }

  .note-card {
    display: block;
    padding: 1.05rem 1.2rem;
    border: 1px solid var(--n-line);
    border-radius: var(--n-radius);
    background: var(--n-surface);
    box-shadow: 0 1px 2px rgba(31, 37, 40, 0.04);
    text-decoration: none !important;
    transition: border-color 0.16s ease, box-shadow 0.16s ease, transform 0.16s ease;
  }

  .note-card[hidden] {
    display: none;
  }

  .note-card:hover {
    border-color: rgba(193, 95, 60, 0.45);
    box-shadow: var(--n-shadow);
    transform: translateY(-2px);
    text-decoration: none !important;
  }

  .note-card__meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem 0.5rem;
    align-items: center;
    margin-bottom: 0.5rem;
    color: var(--n-muted);
    font-size: 0.74rem;
  }

  .note-card__date {
    color: var(--n-accent-2);
    font-weight: 700;
    font-variant-numeric: tabular-nums;
  }

  .note-card__kind {
    display: inline-flex;
    align-items: center;
    gap: 0.38rem;
    color: var(--n-accent);
    font-weight: 700;
  }

  .note-card__kind::before {
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--n-accent);
  }

  .note-card__title {
    margin: 0 0 0.45rem;
    color: var(--n-ink);
    font-family: var(--n-sans);
    font-size: 1.12rem;
    font-weight: 700;
    line-height: 1.4;
    transition: color 0.16s ease;
  }

  .note-card:hover .note-card__title {
    color: var(--n-accent);
  }

  .note-card__summary {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin: 0 0 0.8rem;
    color: var(--n-soft-ink);
    font-size: 0.9rem;
    line-height: 1.7;
  }

  .note-card__tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
  }

  .note-card__tag {
    padding: 0.13rem 0.5rem;
    border: 1px solid rgba(193, 95, 60, 0.22);
    border-radius: 7px;
    background: var(--n-accent-soft);
    color: var(--n-accent-ink);
    font-size: 0.7rem;
    line-height: 1.5;
  }

  .notes-empty {
    padding: 1rem 1.1rem;
    border: 1px dashed var(--n-line);
    border-radius: var(--n-radius);
    background: var(--n-accent-2-soft);
    color: var(--n-muted);
    font-size: 0.9rem;
  }

  /* ---------- pagination ---------- */
  .notes-pagination {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-end;
    gap: 0.4rem;
    margin-top: 1.2rem;
  }

  .notes-page-button {
    min-width: 2.1rem;
    min-height: 2.1rem;
    padding: 0.3rem 0.6rem;
    border: 1px solid var(--n-line);
    border-radius: 8px;
    background: var(--n-surface);
    color: var(--n-muted);
    cursor: pointer;
    font-size: 0.82rem;
    transition: color 0.15s ease, border-color 0.15s ease, background 0.15s ease;
  }

  .notes-page-button:hover:not(:disabled) {
    border-color: var(--n-accent);
    color: var(--n-accent);
  }

  .notes-page-button.is-active {
    border-color: var(--n-accent);
    background: var(--n-accent);
    color: #fff;
  }

  .notes-page-button:disabled {
    cursor: not-allowed;
    opacity: 0.45;
  }

  @media (max-width: 600px) {
    .notes-index {
      padding: 18px;
      border-radius: 14px;
    }

    .notes-toolbar {
      align-items: stretch;
      flex-direction: column;
    }

    .notes-search {
      width: 100%;
    }
  }
</style>

<div class="notes-index" data-page-size="10">
  <header class="notes-hero">
    <p class="notes-hero__kicker">Notes · 站内长文</p>
    <h1 class="notes-hero__title">技术笔记、论文精读与访谈深读</h1>
    <p class="notes-lead">这里整理较长的技术笔记、论文精读、访谈深读和可独立访问的学习资源，按最近更新时间倒序排列。可以用下面的搜索和分类，快速定位想看的主题。</p>
  </header>

  <div class="notes-panel">
    <div class="notes-toolbar">
      <div class="notes-count">
        <span data-notes-visible-count>{{ notes | size }}</span>
        · 每页 10 条
      </div>
      <input class="notes-search" type="search" placeholder="搜索标题、标签或摘要" aria-label="Search notes" data-notes-search>
    </div>

    <div class="notes-filters" aria-label="Note categories">
      <button class="notes-filter-button is-active" type="button" data-note-filter="all" aria-pressed="true">
        全部 <span class="notes-filter-button__count">{{ notes | size }}</span>
      </button>
      {% for group in grouped_notes %}
        <button class="notes-filter-button" type="button" data-note-filter="{{ group.name | slugify }}" aria-pressed="false">
          {{ group.name }} <span class="notes-filter-button__count">{{ group.items | size }}</span>
        </button>
      {% endfor %}
    </div>

    <p class="notes-sort-note">默认排序：最近更新优先；分类筛选和搜索会保留这个倒序。</p>
  </div>

  <div class="notes-list" id="notes-list">
    {% for note in notes %}
      {% capture note_search %}
        {{ note.title }} {{ note.summary }} {{ note.kind }} {{ note.meta }}
        {% for tag in note.tags %} {{ tag }}{% endfor %}
      {% endcapture %}
      <a class="note-card" href="{{ note.url | prepend: base_path }}" data-note-card data-note-kind="{{ note.kind | slugify }}" data-note-search="{{ note_search | strip_newlines | downcase | escape }}">
        <div class="note-card__meta">
          <span class="note-card__date">{{ note.date | date: "%Y-%m-%d" }}</span>
          <span>·</span>
          <span class="note-card__kind">{{ note.kind }}</span>
          {% if note.meta %}
            <span>·</span>
            <span>{{ note.meta }}</span>
          {% endif %}
        </div>
        <h2 class="note-card__title">{{ note.title }}</h2>
        <p class="note-card__summary">{{ note.summary }}</p>
        {% if note.tags %}
          <div class="note-card__tags" aria-label="Tags">
            {% for tag in note.tags %}
              <span class="note-card__tag">{{ tag }}</span>
            {% endfor %}
          </div>
        {% endif %}
      </a>
    {% endfor %}
  </div>

  <div class="notes-empty" data-notes-empty hidden>没有匹配的笔记。</div>

  <nav class="notes-pagination" id="notes-pagination" aria-label="Notes pagination"></nav>
</div>

<script>
  (function () {
    var root = document.querySelector(".notes-index");
    if (!root) return;

    var pageSize = parseInt(root.getAttribute("data-page-size"), 10) || 10;
    var cards = Array.prototype.slice.call(root.querySelectorAll("[data-note-card]"));
    var filters = Array.prototype.slice.call(root.querySelectorAll("[data-note-filter]"));
    var search = root.querySelector("[data-notes-search]");
    var visibleCount = root.querySelector("[data-notes-visible-count]");
    var emptyState = root.querySelector("[data-notes-empty]");
    var pagination = root.querySelector("#notes-pagination");
    var currentPage = 1;
    var activeFilter = "all";
    var query = "";

    function getMatches() {
      return cards.filter(function (card) {
        var kind = card.getAttribute("data-note-kind");
        var haystack = card.getAttribute("data-note-search") || "";
        var filterMatches = activeFilter === "all" || kind === activeFilter;
        var queryMatches = !query || haystack.indexOf(query) !== -1;
        return filterMatches && queryMatches;
      });
    }

    function createButton(label, page, isActive, isDisabled) {
      var button = document.createElement("button");
      button.className = "notes-page-button" + (isActive ? " is-active" : "");
      button.type = "button";
      button.textContent = label;
      button.disabled = isDisabled;
      button.setAttribute("aria-label", "Go to notes page " + page);
      if (isActive) button.setAttribute("aria-current", "page");
      button.addEventListener("click", function () {
        if (!isDisabled) render(page);
      });
      return button;
    }

    function render(page) {
      var matches = getMatches();
      var totalPages = Math.max(1, Math.ceil(matches.length / pageSize));
      currentPage = Math.min(Math.max(page, 1), totalPages);
      var start = (currentPage - 1) * pageSize;
      var end = start + pageSize;
      var pageCards = matches.slice(start, end);

      cards.forEach(function (card) {
        card.hidden = true;
      });
      pageCards.forEach(function (card) {
        card.hidden = false;
      });

      if (visibleCount) visibleCount.textContent = matches.length + " / " + cards.length + " 条";
      if (emptyState) emptyState.hidden = matches.length !== 0;

      pagination.innerHTML = "";
      if (totalPages <= 1) return;

      pagination.appendChild(createButton("上一页", currentPage - 1, false, currentPage === 1));
      for (var pageNumber = 1; pageNumber <= totalPages; pageNumber += 1) {
        pagination.appendChild(createButton(String(pageNumber), pageNumber, pageNumber === currentPage, false));
      }
      pagination.appendChild(createButton("下一页", currentPage + 1, false, currentPage === totalPages));
    }

    filters.forEach(function (button) {
      button.addEventListener("click", function () {
        activeFilter = button.getAttribute("data-note-filter") || "all";
        filters.forEach(function (candidate) {
          var isActive = candidate === button;
          candidate.classList.toggle("is-active", isActive);
          candidate.setAttribute("aria-pressed", isActive ? "true" : "false");
        });
        render(1);
      });
    });

    if (search) {
      search.addEventListener("input", function () {
        query = search.value.toLowerCase().trim();
        render(1);
      });
    }

    render(currentPage);
  }());
</script>

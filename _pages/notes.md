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
  .notes-index {
    --notes-ink: #262b31;
    --notes-muted: #66717d;
    --notes-line: #e1e5ea;
    --notes-accent: #1f5f74;
    --notes-accent-2: #8a5a22;
    --notes-accent-soft: #e8f2f4;
    --notes-warm: #fbf7ef;
  }

  .notes-lead {
    max-width: 48rem;
    margin: 0 0 1.35rem;
    color: var(--notes-muted);
    font-size: 0.98rem;
    line-height: 1.65;
  }

  .notes-panel {
    margin-bottom: 1.1rem;
    padding: 0.9rem 0;
    border-top: 1px solid var(--notes-line);
    border-bottom: 1px solid var(--notes-line);
  }

  .notes-toolbar {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 0.75rem;
    align-items: center;
    margin-bottom: 0.8rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }

  .notes-count {
    color: var(--notes-muted);
    font-size: 0.85rem;
  }

  .notes-search {
    width: min(100%, 19rem);
    min-height: 2.15rem;
    padding: 0.42rem 0.65rem;
    border: 1px solid var(--notes-line);
    border-radius: 6px;
    background: #fff;
    color: var(--notes-ink);
    font: inherit;
  }

  .notes-search:focus {
    outline: 2px solid rgba(31, 95, 116, 0.18);
    border-color: rgba(31, 95, 116, 0.56);
  }

  .notes-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }

  .notes-filter-button {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    min-height: 2rem;
    padding: 0.25rem 0.58rem;
    border: 1px solid var(--notes-line);
    border-radius: 6px;
    background: #fff;
    color: #56616d;
    cursor: pointer;
    font: inherit;
    font-size: 0.78rem;
    line-height: 1.35;
  }

  .notes-filter-button:hover,
  .notes-filter-button.is-active {
    border-color: rgba(31, 95, 116, 0.62);
    background: var(--notes-accent);
    color: #fff;
  }

  .notes-filter-button__count {
    opacity: 0.78;
  }

  .notes-sort-note {
    margin: 0.72rem 0 0;
    color: var(--notes-muted);
    font-size: 0.8rem;
  }

  .notes-list {
    display: grid;
    gap: 0.85rem;
  }

  .note-card {
    display: block;
    padding: 1rem 1.05rem;
    border: 1px solid var(--notes-line);
    border-radius: 8px;
    background: #fff;
    text-decoration: none !important;
    transition: border-color 0.16s ease, box-shadow 0.16s ease, transform 0.16s ease;
  }

  .note-card[hidden] {
    display: none;
  }

  .note-card:hover {
    border-color: rgba(31, 95, 116, 0.42);
    box-shadow: 0 10px 26px rgba(27, 38, 55, 0.08);
    transform: translateY(-1px);
    text-decoration: none !important;
  }

  .note-card__meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    align-items: center;
    margin-bottom: 0.45rem;
    color: var(--notes-muted);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 0.76rem;
  }

  .note-card__kind {
    color: var(--notes-accent);
    font-weight: 700;
  }

  .note-card__date {
    color: var(--notes-accent-2);
    font-weight: 700;
  }

  .note-card__title {
    margin: 0 0 0.45rem;
    color: var(--notes-ink);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 1.08rem;
    line-height: 1.35;
  }

  .note-card__summary {
    margin: 0 0 0.75rem;
    color: #4f5963;
    font-size: 0.9rem;
    line-height: 1.65;
  }

  .note-card__tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
  }

  .note-card__tag {
    padding: 0.12rem 0.45rem;
    border: 1px solid rgba(31, 95, 116, 0.18);
    border-radius: 6px;
    background: var(--notes-accent-soft);
    color: #315f6b;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 0.72rem;
    line-height: 1.45;
  }

  .notes-empty {
    padding: 1rem;
    border: 1px solid var(--notes-line);
    border-radius: 8px;
    background: var(--notes-warm);
    color: var(--notes-muted);
    font-size: 0.9rem;
  }

  .notes-pagination {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-end;
    gap: 0.4rem;
    margin-top: 1rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }

  .notes-page-button {
    min-width: 2rem;
    min-height: 2rem;
    padding: 0.25rem 0.55rem;
    border: 1px solid var(--notes-line);
    border-radius: 6px;
    background: #fff;
    color: var(--notes-muted);
    cursor: pointer;
    font-size: 0.82rem;
  }

  .notes-page-button:hover,
  .notes-page-button.is-active {
    border-color: var(--notes-accent);
    background: var(--notes-accent);
    color: #fff;
  }

  .notes-page-button:disabled {
    cursor: not-allowed;
    opacity: 0.45;
  }

  @media (max-width: 520px) {
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
  <p class="notes-lead">这里整理较长的技术笔记、论文精读和可独立访问的学习资源。列表统一在站内 Notes 页面管理，按最近更新时间倒序排列。</p>

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

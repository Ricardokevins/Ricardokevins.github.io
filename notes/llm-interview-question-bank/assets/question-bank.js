
const buttons = Array.from(document.querySelectorAll('.filter-btn'));
const searchInputs = [document.getElementById('searchInput'), document.getElementById('mobileSearch')].filter(Boolean);
const cards = Array.from(document.querySelectorAll('.chapter-card'));
const links = Array.from(document.querySelectorAll('.toc-link'));
const chapterSections = Array.from(document.querySelectorAll('.chapter-section'));
const tocGroups = Array.from(document.querySelectorAll('#toc .toc-group'));
let activeCategory = 'all';
let query = '';

function normalize(text) {
  return (text || '').toLowerCase().replace(/\s+/g, ' ').trim();
}

function applyFilters() {
  const q = normalize(query);
  cards.forEach(card => {
    const matchCategory = activeCategory === 'all' || card.dataset.category === activeCategory;
    const matchQuery = !q || normalize(card.dataset.search).includes(q);
    card.style.display = matchCategory && matchQuery ? '' : 'none';
  });
  links.forEach(link => {
    const matchCategory = activeCategory === 'all' || link.dataset.category === activeCategory;
    const matchQuery = !q || normalize(link.textContent).includes(q);
    link.style.display = matchCategory && matchQuery ? '' : 'none';
  });
  chapterSections.forEach(section => {
    const visibleCards = Array.from(section.querySelectorAll('.chapter-card')).some(card => card.style.display !== 'none');
    section.style.display = visibleCards ? '' : 'none';
  });
  tocGroups.forEach(group => {
    const groupLinks = Array.from(group.querySelectorAll('.toc-link'));
    if (!groupLinks.length) return;
    const visibleLinks = groupLinks.some(link => link.style.display !== 'none');
    group.style.display = visibleLinks ? '' : 'none';
  });
}

buttons.forEach(button => {
  button.addEventListener('click', () => {
    activeCategory = button.dataset.category;
    buttons.forEach(item => item.classList.toggle('active', item === button));
    applyFilters();
  });
});

searchInputs.forEach(input => {
  input.addEventListener('input', () => {
    query = input.value;
    searchInputs.forEach(other => {
      if (other !== input) other.value = input.value;
    });
    applyFilters();
  });
});

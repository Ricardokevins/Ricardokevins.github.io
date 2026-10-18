const input = document.getElementById('problem-search');
const problems = [...document.querySelectorAll('.problem')];
const categories = [...document.querySelectorAll('.category')];
function filterProblems() {
  const query = input.value.trim().toLowerCase();
  let matches = 0;
  for (const problem of problems) {
    problem.hidden = query !== '' && !problem.dataset.search.toLowerCase().includes(query);
    if (!problem.hidden) matches++;
  }
  for (const category of categories) {
    category.hidden = ![...category.querySelectorAll('.problem')].some(problem => !problem.hidden);
  }
  document.getElementById('match-count').textContent = `${matches} / 100 道题`;
}
input.addEventListener('input', filterProblems);
document.getElementById('show-all').addEventListener('click', () => {
  input.value = '';
  filterProblems();
});
window.addEventListener('beforeprint', () => {
  for (const item of [...problems, ...categories]) item.hidden = false;
});
window.addEventListener('afterprint', filterProblems);

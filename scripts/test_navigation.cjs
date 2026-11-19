const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'assets/js/plugins/jquery.greedy-navigation.js'), 'utf8');

function navigation(width, itemCount) {
  const visible = Array.from({ length: itemCount }, (_, index) => index);
  const hidden = [];
  const classes = new Set();
  const button = {
    hasClass: name => classes.has(name),
    width: () => 30,
    addClass: name => classes.add(name),
    removeClass: name => classes.delete(name),
    attr: () => {},
    on: () => {}
  };
  function links(items) {
    return {
      width: () => items.length * 100,
      addClass: () => {},
      toggleClass: () => {},
      children: () => ({
        length: items.length,
        last: () => ({ prependTo: () => { if (items.length) hidden.unshift(items.pop()); } }),
        first: () => ({ appendTo: () => { if (items.length) visible.push(items.shift()); } })
      })
    };
  }
  const window = {};
  const context = vm.createContext({
    window,
    $: selector => selector === window ? { resize: () => {} } : {
      '#site-nav': { width: () => width },
      '#site-nav button': button,
      '#site-nav .visible-links': links(visible),
      '#site-nav .hidden-links': links(hidden)
    }[selector]
  });
  vm.runInContext(source, context, { timeout: 1000 });
  return { context, visible, hidden, classes, resize: value => { width = value; context.updateNav(); } };
}

test('zero-width navigation terminates and never records nonexistent items', () => {
  const state = navigation(0, 5);
  assert.equal(state.visible.length, 0);
  assert.equal(state.hidden.length, 5);
  assert.equal(state.context.breaks.length, 5);
  state.resize(0);
  assert.equal(state.context.breaks.length, 5);
});

test('empty navigation terminates in negative available space', () => {
  assert.equal(navigation(0, 0).context.breaks.length, 0);
});

test('resize restores original item order and hides the empty dropdown', () => {
  const state = navigation(180, 5);
  assert.equal(state.visible.length, 1);
  for (let index = 0; index < 6; index += 1) state.resize(1000);
  assert.deepEqual(state.visible, [0, 1, 2, 3, 4]);
  assert.deepEqual(state.hidden, []);
  assert.equal(state.context.breaks.length, 0);
  assert.ok(state.classes.has('hidden'));
});

test('footer resize uses one pending timeout and no perpetual timer', () => {
  const main = fs.readFileSync(path.join(root, 'assets/js/_main.js'), 'utf8');
  assert.doesNotMatch(main, /setInterval\(/);
  assert.match(main, /clearTimeout\(resizeTimer\)/);
  assert.match(main, /setTimeout\(bumpIt, 250\)/);
});

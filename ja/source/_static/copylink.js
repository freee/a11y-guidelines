document.addEventListener('DOMContentLoaded', function () {
  const currentLang = document.documentElement.lang || 'ja';
  const labels = languageResources[currentLang];    

  const firstH1 = document.querySelector('h1');
  if (firstH1) {
    appendDropdownMenu(firstH1, firstH1.textContent, location.origin + location.pathname);
  }

  document.querySelectorAll('section.permalink').forEach(section => {
    const firstHeader = section.querySelector('h1, h2, h3, h4, h5, h6');
    if (firstHeader) {
      let id;
      const firstSpan = section.querySelector('span');
      if (firstSpan && firstSpan.id && /id\d+/.test(firstSpan.id)) {
        id = section.id;
      } else if (firstSpan && firstSpan.id) {
        id = firstSpan.id;
      } else {
        id = section.id;
      }
      const url = location.origin + location.pathname + '#' + id;
      appendDropdownMenu(firstHeader, firstHeader.textContent, url);
    }
  });

  function appendDropdownMenu(element, title, url) {
    const dropdown = document.createElement('div');
    dropdown.className = 'dropdown';

    const button = document.createElement('button');
    button.className = 'copy-link';
    button.textContent = labels['copy'];
    button.setAttribute('aria-haspopup', 'true');
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('tabindex', '0');

    const menu = document.createElement('div');
    menu.className = 'dropdown-menu';
    menu.setAttribute('role', 'menu');
    menu.style.display = 'none';

    const copyUrl = createMenuItem(labels['copyUrl'], () => navigator.clipboard.writeText(url));
    const copyTitleUrl = createMenuItem(labels['copyTitleUrl'], () => navigator.clipboard.writeText(`${title} - ${url}`));

    menu.appendChild(copyUrl);
    menu.appendChild(copyTitleUrl);
    dropdown.appendChild(button);
    dropdown.appendChild(menu);
    element.appendChild(dropdown);

    button.addEventListener('click', function(event) {
      event.stopPropagation();
      toggleDropdown.call(this, event);
    });

    document.addEventListener('keydown', function(event) {
      if (event.key === 'Tab' && menu.style.display === 'block') {
        event.preventDefault();
        moveFocusInMenu(menu, event.shiftKey);
      }
    });

    menu.addEventListener('keydown', function(event) {
      handleMenuKeyDown(event, button, menu);
    });

    function toggleDropdown(event) {
      const isOpen = menu.style.display === 'block';
      menu.style.display = isOpen ? 'none' : 'block';
      this.setAttribute('aria-expanded', !isOpen);
      if (!isOpen) {
        menu.querySelector('[role="menuitem"]').focus();
      } else {
        button.focus();
      }
    }
  }

  function handleMenuKeyDown(event, button, menu) {
    switch (event.key) {
      case 'Escape':
        menu.style.display = 'none';
        button.setAttribute('aria-expanded', 'false');
        button.focus();
        event.preventDefault();
        break;
      case 'ArrowDown':
        moveFocusInMenu(menu, false);
        break;
      case 'ArrowUp':
        moveFocusInMenu(menu, true);
        break;
    }
  }

  function moveFocusInMenu(menu, reverse) {
    const items = menu.querySelectorAll('[role="menuitem"]');
    const currentFocus = document.activeElement;
    const currentIndex = Array.from(items).indexOf(currentFocus);
    const nextIndex = reverse ? (currentIndex - 1 + items.length) % items.length : (currentIndex + 1) % items.length;
    items[nextIndex].focus();
  }

  function createMenuItem(text, action) {
    const item = document.createElement('a');
    item.href = '#';
    item.role = 'menuitem';
    item.textContent = text;
    item.setAttribute('tabindex', '0');
    item.onclick = function(event) {
      event.preventDefault();
      action();
      closeAllDropdowns();
    };
    return item;
  }

  function closeAllDropdowns() {
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
      if (menu.style.display === 'block') {
        menu.style.display = 'none';
        const button = menu.closest('.dropdown').querySelector('.copy-link');
        button.setAttribute('aria-expanded', 'false');
        button.focus();
      }
    });
  }
});

const languageResources = {
  'en': {
    'copy': 'Copy',
    'copyUrl': 'Copy URL',
    'copyTitleUrl': 'Copy Title and URL'
  },
  'ja': {
    'copy': 'コピー',
    'copyUrl': 'URLをコピー',
    'copyTitleUrl': 'タイトルとURLをコピー'
  }
};

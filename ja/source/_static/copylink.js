document.addEventListener('DOMContentLoaded', function () {
  const buttonLabel = 'リンクをコピー';
  function appendCopyButton(element, textToCopy) {
    const button = document.createElement('button');
    button.textContent = buttonLabel;
    button.className = 'copy-link';
    button.onclick = function () {
      navigator.clipboard.writeText(textToCopy);
    };
    element.appendChild(button);
  }

  const firstH1 = document.querySelector('h1');
  if (firstH1) {
    appendCopyButton(firstH1, location.href);
  }

  const sections = document.querySelectorAll('section.permalink');
  sections.forEach(section => {
    const header = section.querySelector('h2, h3, h4, h5, h6');
    if (header) {
      const urlToCopy = location.origin + location.pathname + '#' + section.id;
      appendCopyButton(header, urlToCopy);  // sectionのIDを含むURLを使用
    }
  });
});

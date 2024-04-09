document.addEventListener('DOMContentLoaded', function () {
  const buttonLabel = 'Copy Link';
  const sections = document.querySelectorAll('section.permalink');

  sections.forEach(section => {
    const header = section.querySelector('h2');
    if (header) {
      const button = document.createElement('button');
      button.textContent = buttonLabel;
      button.className = 'copy-link';
      button.onclick = function () {
        navigator.clipboard.writeText(location.origin + location.pathname + '#' + section.id);
      };
      header.appendChild(button);
    }
  });
});

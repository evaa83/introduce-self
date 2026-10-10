// Keep the reading position when moving between the static language versions.
document.querySelectorAll('.language-switch a').forEach((link) => {
  link.addEventListener('click', () => {
    link.hash = window.location.hash;
  });
});

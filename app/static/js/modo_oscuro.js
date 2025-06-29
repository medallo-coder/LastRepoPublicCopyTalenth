  //funcion modo oscuro

   const toggle = document.getElementById('theme-toggle');
  const body = document.body;

  toggle.addEventListener('click', () => {
    // Alternar clase de modo oscuro
    body.classList.toggle('dark-mode');

    // Alternar ícono
    if (toggle.classList.contains('bi-brightness-high-fill')) {
      toggle.classList.remove('bi-brightness-high-fill');
      toggle.classList.add('bi-moon-fill');
    } else {
      toggle.classList.remove('bi-moon-fill');
      toggle.classList.add('bi-brightness-high-fill');
    }
  });
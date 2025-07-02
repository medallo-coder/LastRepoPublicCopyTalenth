document.addEventListener("DOMContentLoaded", () => {
  const deleteLinks = document.querySelectorAll('.btn-danger');

  deleteLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      if (!confirm('¿Seguro que deseas eliminar esta publicación?')) {
        e.preventDefault();
      }
    });
  });
});


function toggleMenu(trigger) {
  const menu = trigger.nextElementSibling;
  document.querySelectorAll('.menu-opciones').forEach(m => {
    if (m !== menu) m.style.display = 'none';
  });
  menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
}

document.addEventListener('click', function(event) {
  if (!event.target.closest('.acciones-menu')) {
    document.querySelectorAll('.menu-opciones').forEach(m => m.style.display = 'none');
  }
});

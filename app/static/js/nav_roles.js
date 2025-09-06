document.addEventListener('DOMContentLoaded', () => {
  const botones = document.querySelectorAll('.btn-cambio-rol');

  botones.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault(); // Detiene el <a href="#">
      const url = btn.getAttribute('data-url');
      const titulo = btn.getAttribute('data-titulo');
      confirmarCambioRol(url, titulo);
    });
  });

  document.getElementById('btnCancelar').addEventListener('click', () => {
    document.getElementById('modalCambioRol').style.display = 'none';
  });

  // 👉 Cerrar modal al hacer clic en el fondo oscuro
  document.getElementById('modalCambioRol').addEventListener('click', (e) => {
    if (e.target === document.getElementById('modalCambioRol')) {
      document.getElementById('modalCambioRol').style.display = 'none';
    }
  });
});

function confirmarCambioRol(url, titulo) {
  document.getElementById('modalCambioRol').style.display = 'flex';
  document.getElementById('modal-title').textContent = titulo;
  document.getElementById('modal-text').textContent = `¿Estás seguro que deseas ${titulo.toLowerCase()}?`;
  document.getElementById('btnAceptar').href = url;
}

//hola aca estan las x
document.querySelector('.modal-close').addEventListener('click', function () {
  document.getElementById('modalCambioRol').style.display = 'none';
});

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
  const modalCambioRol = document.getElementById('modalCambioRol');
  modalCambioRol.addEventListener('click', (e) => {
    if (e.target === modalCambioRol) { // solo si toco el fondo
      modalCambioRol.style.display = 'none';
    }
  });
});

function confirmarCambioRol(url, titulo) {
  document.getElementById('modalCambioRol').style.display = 'flex';
  document.getElementById('modal-title').textContent = "Conviértete en Experto ahora";
  document.getElementById('btnAceptar').href = url;
}


// Modal cerrar sesión
const modalCerrarSesion = document.getElementById('modalCerrarSesion');
const btnCerrarSesion = document.querySelector('.cerrar-li button'); // tu botón cerrar sesión
const btnCancelarCerrar = document.getElementById('btnCancelarCerrar');

// Abrir modal al hacer clic en cerrar sesión
if(btnCerrarSesion){
    btnCerrarSesion.addEventListener('click', function(e){
        e.preventDefault();
        modalCerrarSesion.classList.remove('hidden');
    });
}

// Cerrar modal al hacer clic en cancelar
btnCancelarCerrar.addEventListener('click', () => modalCerrarSesion.classList.add('hidden'));

// 👉 Cerrar modal al hacer clic fuera del contenido
modalCerrarSesion.addEventListener('click', (e) => {
    if(e.target === modalCerrarSesion){ // solo fondo
        modalCerrarSesion.classList.add('hidden');
    }
});


//hola aca estan las x
const btnClose = document.querySelector('.modal-close');
if (btnClose) {
  btnClose.addEventListener('click', function () {
    document.getElementById('modalCambioRol').style.display = 'none';
  });
}

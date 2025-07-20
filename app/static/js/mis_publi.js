// Navegación entre tabs
function activarTab(element) {
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => tab.classList.remove('active'));
  element.classList.add('active');
}

// Menú acciones
function toggleMenu(trigger) {
  const menu = trigger.nextElementSibling;
  document.querySelectorAll('.menu-opciones').forEach(m => {
    if (m !== menu) m.style.display = 'none';
  });
  menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
}

document.addEventListener("DOMContentLoaded", () => {
  // Mostrar formulario al pulsar el botón de nueva publicación
  const mostrarBtn = document.getElementById('mostrarFormulario');
  const card = document.querySelector('.card');
  if (mostrarBtn && card) {
    mostrarBtn.addEventListener('click', () => {
      card.style.display = 'block';
      mostrarBtn.style.display = 'none';
    });
  }

  // Ocultar menús al hacer clic fuera
  document.addEventListener('click', function(event) {
    if (!event.target.closest('.acciones-menu')) {
      document.querySelectorAll('.menu-opciones').forEach(m => m.style.display = 'none');
    }
  });

  // Modal para eliminar
  let enlaceAEliminar = null;

  // Cambié a clase .btn-eliminar-modal para ser más claro y no usar btn-danger que confunde
  document.querySelectorAll('.btn-eliminar-modal').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      enlaceAEliminar = link.getAttribute('data-url');
      const modal = document.getElementById('modalEliminar');
      if (modal) {
        modal.classList.remove('hidden');
      }
    });
  });

  // Botón cerrar
  const cerrarModalBtn = document.getElementById('cerrarModalEliminar');
  if (cerrarModalBtn) {
    cerrarModalBtn.addEventListener('click', () => {
      document.getElementById('modalEliminar').classList.add('hidden');
    });
  }

  // Botón cancelar
  const cancelarBtn = document.getElementById('cancelarEliminar');
  if (cancelarBtn) {
    cancelarBtn.addEventListener('click', () => {
      document.getElementById('modalEliminar').classList.add('hidden');
    });
  }

  // Botón confirmar
  const confirmarBtn = document.getElementById('confirmarEliminar');
  if (confirmarBtn) {
    confirmarBtn.addEventListener('click', () => {
      if (enlaceAEliminar) {
        window.location.href = enlaceAEliminar;
      }
    });
  }

  // Cerrar modal al hacer clic en la sombra
  const modal = document.getElementById('modalEliminar');
  if (modal) {
    modal.addEventListener('click', function(e) {
      if (e.target === this) {
        this.classList.add('hidden');
      }
    });
  }
});

//back de mostrar las catefgorias y subcategorias
document.addEventListener('DOMContentLoaded', () => {
  const categoriaSelect = document.getElementById('categoriaSelect');
  const subcategoriaSelect = document.getElementById('subcategoriaSelect');

  categoriaSelect.addEventListener('change', function () {
    const categoriaId = this.value;

    if (!categoriaId) {
      subcategoriaSelect.innerHTML = '<option value="">Seleccione</option>';
      return;
    }

    fetch(`/subcategorias/${categoriaId}`)
      .then(response => response.json())
      .then(data => {
        subcategoriaSelect.innerHTML = '<option value="">Seleccione</option>';
        data.forEach(sub => {
          const option = document.createElement('option');
          option.value = sub.id;
          option.textContent = sub.nombre;
          subcategoriaSelect.appendChild(option);
        });
      });
  });
});

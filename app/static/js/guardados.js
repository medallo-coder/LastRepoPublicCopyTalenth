
document.addEventListener('DOMContentLoaded', () => {
  // SLIDER (si existe)
  const slider = document.getElementById("slider");
  const buttons = document.querySelectorAll(".arrow-btn");

  if (slider && buttons.length === 2) {
    buttons[0].addEventListener("click", (e) => {
      e.preventDefault();
      slider.scrollLeft -= 300;
    });

    buttons[1].addEventListener("click", (e) => {
      e.preventDefault();
      slider.scrollLeft += 300;
    });
  }

  // MENÚ DESPLEGABLE
  const menuButtons = document.querySelectorAll('.menu-button');
  const dropdownMenus = document.querySelectorAll('.dropdown-menu');

  menuButtons.forEach((button, index) => {
    const dropdownMenu = dropdownMenus[index];

    button.addEventListener('click', (e) => {
      e.stopPropagation();
      const isVisible = dropdownMenu.style.display === 'block';
      dropdownMenus.forEach(menu => menu.style.display = 'none');
      dropdownMenu.style.display = isVisible ? 'none' : 'block';
    });
  });

  document.addEventListener('click', () => {
    dropdownMenus.forEach(menu => menu.style.display = 'none');
  });

  dropdownMenus.forEach(menu => {
    menu.addEventListener('click', (e) => {
      e.stopPropagation();
    });
  });

  // ELIMINAR GUARDADO CON MODAL
  const trashIcons = document.querySelectorAll('.eliminar-guardado');
  const modal = document.getElementById('confirmModal');
  const confirmBtn = document.getElementById('confirmDelete');
  const cancelBtn = document.getElementById('cancelDelete');
  let selectedPubId = null;
  let selectedElement = null;

  trashIcons.forEach(icon => {
    icon.addEventListener('click', () => {
      selectedPubId = icon.dataset.id;
      selectedElement = icon.closest('.categoria');
      modal.style.display = 'flex'; // Mostrar modal
    });
  });

  confirmBtn.addEventListener('click', () => {
    if (!selectedPubId) return;

    fetch(`/mis-guardados/eliminar/${selectedPubId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
      .then(res => res.json())
      .then(data => {
        mostrarMensaje(data.message, data.success ? 'success' : 'danger');

        if (data.success && selectedElement) {
          selectedElement.remove();
          const publicacionesRestantes = document.querySelectorAll('.categoria');
          if (publicacionesRestantes.length === 0) {
            const noGuardados = document.querySelector('.no-guardados');
            if (noGuardados) noGuardados.style.display = 'flex';
          }
        }
      })
      .catch(err => {
        console.error(err);
        mostrarMensaje("Error al eliminar el guardado", "danger");
      })
      .finally(() => {
        modal.style.display = 'none';
        selectedPubId = null;
        selectedElement = null;
      });
  });

  cancelBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    selectedPubId = null;
    selectedElement = null;
  });

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
      selectedPubId = null;
      selectedElement = null;
    }
  });
});

// Función para cerrar el menú al presionar la "x"
function cerrarMenu(elemento) {
  const menu = elemento.closest('.dropdown-menu');
  if (menu) {
    menu.style.display = 'none';
  }
}

// Función para mostrar mensajes
function mostrarMensaje(mensaje, categoria) {
  const container = document.querySelector('.messages-container');
  if (!container) return;

  const alertDiv = document.createElement('div');
  alertDiv.className = `alert ${categoria}`;
  alertDiv.textContent = mensaje;

  container.appendChild(alertDiv);
  setTimeout(() => alertDiv.remove(), 4000);
}

// js de foto para ver en grande
document.addEventListener('DOMContentLoaded', () => {
  const imagenes = document.querySelectorAll('.image');
  const modal = document.getElementById('imagenModal');
  const modalImg = document.getElementById('imagenAmpliada');
  const cerrar = document.getElementById('cerrarModal');

  imagenes.forEach(img => {
    img.addEventListener('click', () => {
      modal.style.display = 'flex';
      modalImg.src = img.src;
    });
  });

  cerrar.addEventListener('click', () => {
    modal.style.display = 'none';
  });
});


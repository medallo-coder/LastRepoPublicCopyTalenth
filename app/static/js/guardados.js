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

  // Cierra los menús al hacer clic fuera
  document.addEventListener('click', () => {
    dropdownMenus.forEach(menu => menu.style.display = 'none');
  });

  // Prevenir cierre si clic dentro
  dropdownMenus.forEach(menu => {
    menu.addEventListener('click', (e) => {
      e.stopPropagation();
    });
  });

  // Evitar que los <a href="#"> hagan scroll arriba
  const links = document.querySelectorAll('.dropdown-menu a');
  links.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
    });
  });
});
document.addEventListener('DOMContentLoaded', () => {
  const trashIcons = document.querySelectorAll('.eliminar-guardado');

  trashIcons.forEach(icon => {
    icon.addEventListener('click', () => {
      const pubId = icon.dataset.id;

      // Enviamos el POST con fetch
      fetch(`/mis-guardados/eliminar/${pubId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(res => res.json())
      .then(data => {
        // Muestra el mensaje usando tu sistema dinámico
        mostrarMensaje(data.message, data.success ? 'success' : 'danger');

        if (data.success) {
          // Elimina el bloque de la publicación eliminada sin recargar
          icon.closest('.categoria').remove();
        }
      })
      .catch(err => {
        console.error(err);
        mostrarMensaje("Error al eliminar el guardado", "danger");
      });
    });
  });

  // Sistema de menú desplegable (igual como lo tienes)
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

  const links = document.querySelectorAll('.dropdown-menu a');
  links.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
    });
  });
});

// Función para inyectar mensaje al contenedor dinámico
function mostrarMensaje(mensaje, categoria) {
  const container = document.querySelector('.messages-container');
  if (!container) return;

  const alertDiv = document.createElement('div');
  alertDiv.className = `alert ${categoria}`;
  alertDiv.textContent = mensaje;

  container.appendChild(alertDiv);

  // Que desaparezca luego de unos segundos
  setTimeout(() => {
    alertDiv.remove();
  }, 4000);
}

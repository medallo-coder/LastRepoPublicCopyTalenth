
 //Navegacion
function activarTab(element) {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    element.classList.add('active');
  }


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




// --- Lógica para las tarjetas (descripción y "Ver Más", existente, se mantiene) ---
    document.addEventListener("DOMContentLoaded", () => {
  // Confirmación al eliminar
  const deleteLinks = document.querySelectorAll('.btn-danger');
  deleteLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      if (!confirm('¿Seguro que deseas eliminar esta publicación?')) {
        e.preventDefault();
      }
    });
  });

  // Lógica de menú
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

  // Lógica de las tarjetas "Ver Más"
  const tarjetas = document.querySelectorAll('.card-tarjeta');
  tarjetas.forEach(tarjeta => {
    const descripcionElem = tarjeta.querySelector('.descripcion');
    const verMasBtn = tarjeta.querySelector('.ver-mas');
    if (!descripcionElem || !verMasBtn) return;

    const textoOriginal = descripcionElem.textContent.trim();

    if (textoOriginal.length > 70) {
      descripcionElem.textContent = textoOriginal.substring(0, 70) + '...';
      verMasBtn.classList.remove('hidden');

      verMasBtn.addEventListener('click', () => {
        const tarjetaClonada = tarjeta.cloneNode(true);
        tarjetaClonada.querySelector('.descripcion').textContent = textoOriginal;

        const verMasClon = tarjetaClonada.querySelector('.ver-mas');
        if (verMasClon) verMasClon.remove();

        const menuClon = tarjetaClonada.querySelector('.menu-button-container');
        if (menuClon) menuClon.remove();

        const contenedorModal = document.getElementById('contenidoTarjeta');
        if (contenedorModal) {
          contenedorModal.innerHTML = '';
          contenedorModal.appendChild(tarjetaClonada);
        }

        const modalTarjeta = document.getElementById('modalTarjeta');
        if (modalTarjeta) {
          modalTarjeta.classList.remove('hidden');
        }
      });
    } else {
      verMasBtn.classList.add('hidden');
    }
  });

  const cerrarTarjetaBtn = document.getElementById('cerrarTarjeta');
  if (cerrarTarjetaBtn) {
    cerrarTarjetaBtn.addEventListener('click', () => {
      const modalTarjeta = document.getElementById('modalTarjeta');
      if (modalTarjeta) {
        modalTarjeta.classList.add('hidden');
      }
    });
  }
});

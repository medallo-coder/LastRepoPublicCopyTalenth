document.addEventListener("DOMContentLoaded", () => {
  // ---------------------------
  // Tabs
  // ---------------------------
  const tabs = document.querySelectorAll(".tabs__tab");
  const active = document.querySelector(".active_tab");
  let currentTab = 0;

  const move = (target, ac) => {
    const { offsetLeft, offsetTop, offsetWidth, offsetHeight } = target;
    active.style.left = `${offsetLeft}px`;
    active.style.top = `${offsetTop}px`;
    active.style.width = `${offsetWidth}px`;
    active.style.height = `${offsetHeight}px`;
    currentTab = ac;
  };

  // Detectar tab actual
  tabs.forEach((tab, index) => {
    if (window.location.pathname === tab.dataset.href) {
      currentTab = index;
    }
  });

  // Posicionar cuadro al cargar
  if (tabs.length > 0) move(tabs[currentTab], currentTab);

  tabs.forEach((el, index) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      move(el, index);
      const href = el.dataset.href;
      setTimeout(() => {
        window.location.href = href;
      }, 300);
    });
  });

  window.addEventListener("resize", () => {
    if (tabs.length > 0) move(tabs[currentTab], currentTab);
  });

  // ---------------------------
  // Menú acciones
  // ---------------------------
  function toggleMenu(trigger) {
    const menu = trigger.nextElementSibling;
    document.querySelectorAll('.menu-completo').forEach(m => {
      if (m !== menu) m.style.display = 'none';
    });
    menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
  }
  window.toggleMenu = toggleMenu; // Para poder usar en HTML con onclick

  document.addEventListener('click', function(event) {
    if (!event.target.closest('.acciones-menu')) {
      document.querySelectorAll('.menu-completo').forEach(m => m.style.display = 'none');
    }
  });

  // ---------------------------
  // Mostrar formulario nueva publicación
  // ---------------------------
  const mostrarBtn = document.getElementById('mostrarFormulario');
  const card = document.querySelector('.card');
  if (mostrarBtn && card) {
    mostrarBtn.addEventListener('click', () => {
      card.style.display = 'block';
      mostrarBtn.style.display = 'none';
    });
  }

  // ---------------- MODAL ELIMINAR ----------------
const modalEliminar = document.getElementById("modalEliminar");
const btnCancelarEliminar = document.getElementById("cancelEliminar");
const btnConfirmarEliminar = document.getElementById("confirmEliminar");

let urlEliminar = null; // Guardará la URL del elemento a eliminar

// Abrir modal al hacer clic en cualquier botón de eliminar
document.querySelectorAll(".btn-eliminar-modal").forEach(btn => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    urlEliminar = btn.dataset.url; // Obtenemos la URL de eliminación
    modalEliminar.classList.remove("hidden");
  });
});

// Cerrar modal con el botón Cancelar
btnCancelarEliminar.addEventListener("click", () => {
  modalEliminar.classList.add("hidden");
});

// Confirmar eliminación
btnConfirmarEliminar.addEventListener("click", () => {
  if (urlEliminar) {
    window.location.href = urlEliminar; // Ejecuta la eliminación
  }
});

// Cerrar modal al hacer clic fuera del contenido
modalEliminar.addEventListener("click", (e) => {
  if (e.target === modalEliminar) {
    modalEliminar.classList.add("hidden");
  }
});



  // ---------------------------
  // Categorías y Subcategorías
  // ---------------------------
  const categoriaSelect = document.getElementById('categoriaSelect');
  const subcategoriaSelect = document.getElementById('subcategoriaSelect');

  if (categoriaSelect && subcategoriaSelect) {
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
  }

  // ---------------------------
  // Contador caracteres descripción
  // ---------------------------
  const textarea = document.getElementById('descripcion');
  const contador = document.getElementById('contadorCaracteres');
  const maxCaracteres = 200;

  if (textarea && contador) {
    contador.textContent = `${textarea.value.length}/${maxCaracteres} caracteres`;

    textarea.addEventListener('input', () => {
      let texto = textarea.value;

      if (texto.length > maxCaracteres) {
        texto = texto.substring(0, maxCaracteres);
        textarea.value = texto;
      }

      contador.textContent = `${texto.length}/${maxCaracteres} caracteres`;

      contador.classList.remove('limit-reached', 'warning');
      if (texto.length >= maxCaracteres) {
        contador.classList.add('limit-reached');
      } else if (texto.length >= maxCaracteres - 20) {
        contador.classList.add('warning');
      }
    });
  }
});

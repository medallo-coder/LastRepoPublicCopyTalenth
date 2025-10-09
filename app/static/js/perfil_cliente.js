// Navegacion
function activarTab(element) {
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => tab.classList.remove('active'));
  element.classList.add('active');
}

// Función para abrir y cerrar formularios
function accionLapiz() {
  document.getElementById('formulario-editar').style.display = 'flex';
}

function cerrarFormulario() {
  document.getElementById('formulario-editar').style.display = 'none';
}

function mostrarFormularioUbicacion() {
  document.getElementById('formularioUbicacion').style.display = 'flex';
}

function cerrarFormularioUbicacion() {
  document.getElementById('formularioUbicacion').style.display = 'none';
}

function cerrarFormularioEditarUbicacion() {
  document.getElementById('formularioUbicacionEditar').style.display = 'none';
}

function mostrarFormularioEmpresa() {
  document.getElementById('formulario-empresa').style.display = 'flex';
}

function cerrarFormularioEmpresa() {
  document.getElementById('formulario-empresa').style.display = 'none';
}

function cerrarFormularioEditarEmpresa() {
  document.getElementById('formulario-editar-empresa').style.display = 'none';
}

document.addEventListener("DOMContentLoaded", function () {
  // Lógica para editar ubicación
  document.getElementById('lapizubicacion')?.addEventListener('click', function () {
    const item = this.closest('.item-ubicacion');
    const barrio = item.querySelector('.barrio')?.innerText;
    document.getElementById('editar-barrio').value = barrio;
    document.getElementById('formularioUbicacionEditar').style.display = 'flex';
  });

  // Lógica para editar empresa
  document.getElementById('lapizempresa')?.addEventListener('click', function () {
    const item = this.closest('.item-empresa');
    const empresa = item.querySelector('.nombre_empresa')?.innerText;
    document.getElementById('editar-empresa').value = empresa;
    document.getElementById('formulario-editar-empresa').style.display = 'flex';
  });
// === Calificaciones ===
const slider = document.getElementById("slider");
const arrowButtons = document.querySelectorAll(".arrow-btn");

function getScrollAmount() {
  return window.innerWidth <= 480 ? 365 : 600;
}

arrowButtons[0]?.addEventListener("click", () => {
  slider.scrollBy({ left: -getScrollAmount(), behavior: "smooth" });
});

arrowButtons[1]?.addEventListener("click", () => {
  slider.scrollBy({ left: getScrollAmount(), behavior: "smooth" });
});

// === Mostrar/ocultar flechas según cantidad de tarjetas y tamaño de pantalla ===
function actualizarFlechas() {
  const arrows = document.querySelector(".arrows");
  const cards = slider?.querySelectorAll(".card") || [];

  if (!slider || !arrows) return;

  // Si no hay calificaciones, ocultar flechas
  if (cards.length === 0) {
    arrows.style.display = "none";
    return;
  }

  // Medir el ancho total del contenido y el área visible
  const totalWidth = slider.scrollWidth;
  const visibleWidth = slider.clientWidth;

  // Mostrar u ocultar flechas según sea necesario
  if (totalWidth > visibleWidth) {
    arrows.style.display = "flex";
  } else {
    arrows.style.display = "none";
  }
}

// Ejecutar al cargar la página
actualizarFlechas();

// Volver a ejecutar si cambia el tamaño de la pantalla
window.addEventListener("resize", actualizarFlechas);

  // Menús
  const menuButtons = document.querySelectorAll('.menu-button');
  const dropdownMenus = document.querySelectorAll('.dropdown-menu');

  menuButtons.forEach((button, index) => {
    const dropdownMenu = dropdownMenus[index];

    button.addEventListener('click', (e) => {
      e.stopPropagation();
      const isVisible = dropdownMenu.style.display === 'block';
      dropdownMenus.forEach(menu => (menu.style.display = 'none'));
      dropdownMenu.style.display = isVisible ? 'none' : 'block';
    });
  });

  document.addEventListener('click', () => {
    dropdownMenus.forEach(menu => (menu.style.display = 'none'));
  });

  dropdownMenus.forEach(menu => {
    menu.addEventListener('click', (e) => {
      e.stopPropagation();
    });
  });

  // Tarjetas
  const tarjetas = document.querySelectorAll('.tarjeta');

  tarjetas.forEach(tarjeta => {
    const descripcionElem = tarjeta.querySelector('.descripcion');
    const verMasBtn = tarjeta.querySelector('.ver-mas');
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
        contenedorModal.innerHTML = '';
        contenedorModal.appendChild(tarjetaClonada);

        document.getElementById('modalTarjeta').classList.remove('hidden');
      });
    } else {
      verMasBtn.classList.add('hidden');
    }
  });

  // Cierre del modal de tarjeta
  document.getElementById('cerrarTarjeta')?.addEventListener('click', () => {
    document.getElementById('modalTarjeta').classList.add('hidden');
  });

  const modalTarjeta = document.getElementById("modalTarjeta");
  const contenidoTarjeta = modalTarjeta?.querySelector(".modal-content");

  if (modalTarjeta && contenidoTarjeta) {
    modalTarjeta.addEventListener("click", (e) => {
      if (!contenidoTarjeta.contains(e.target)) {
        modalTarjeta.classList.add("hidden");
      }
    });

    contenidoTarjeta.addEventListener("click", (e) => {
      e.stopPropagation();
    });
  }

  // Cierre automático de formularios si se hace clic fuera del contenido
  const formularios = [
    { id: "formulario-editar", contenido: ".formulario-contenido" },
    { id: "formularioUbicacion", contenido: ".formulario-ubicacion-contenido" },
    { id: "formularioUbicacionEditar", contenido: ".formulario-editar-ubicacion-contenido" },
    { id: "formulario-empresa", contenido: ".formulario-empresa-contenido" },
    { id: "formulario-editar-empresa", contenido: ".formulario-editar-empresa-contenido" }
  ];

  formularios.forEach(({ id, contenido }) => {
    const fondo = document.getElementById(id);
    if (!fondo) return;

    const interior = fondo.querySelector(contenido);
    if (!interior) return;

    fondo.addEventListener("click", (e) => {
      if (!interior.contains(e.target)) {
        fondo.style.display = "none";
      }
    });

    interior.addEventListener("click", (e) => {
      e.stopPropagation();
    });
  });

  
  // Modal eliminar barrio
const btnEliminarBarrio = document.getElementById("btnEliminarBarrio");
const modalEliminarBarrio = document.getElementById("modalEliminarBarrio");
const confirmEliminarBarrio = document.getElementById("confirmEliminarBarrio");
const cancelEliminarBarrio = document.getElementById("cancelEliminarBarrio");
const formEliminarBarrio = document.getElementById("formEliminarBarrio");

if (btnEliminarBarrio && modalEliminarBarrio && formEliminarBarrio) {
  // Abrir modal al hacer clic en el icono de basura
  btnEliminarBarrio.addEventListener("click", () => {
    modalEliminarBarrio.classList.remove("hidden");
  });

  // Confirmar eliminación: enviar formulario
  confirmEliminarBarrio.addEventListener("click", () => {
    formEliminarBarrio.submit();
  });

  // Cancelar eliminación: cerrar modal
  cancelEliminarBarrio.addEventListener("click", () => {
    modalEliminarBarrio.classList.add("hidden");
  });

  // Cerrar modal si se hace clic fuera del contenido
  modalEliminarBarrio.addEventListener("click", (e) => {
    if (!e.target.closest(".modal-content-delete")) {
      modalEliminarBarrio.classList.add("hidden");
    }
  });
}

});

// Foto de perfil
function mostrarImagen(event) {
  const input = event.target;
  const reader = new FileReader();

  reader.onload = function () {
    const preview = document.getElementById('preview');
    preview.style.backgroundImage = `url(${reader.result})`;
    preview.innerHTML = '';
  };

  if (input.files[0]) {
    reader.readAsDataURL(input.files[0]);
    setTimeout(() => {
      document.getElementById('formImagen').submit();
    }, 500);
  }
}

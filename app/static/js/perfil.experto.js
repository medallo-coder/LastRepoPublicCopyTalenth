//tabs
// === Tabs ===
const tabs = document.querySelectorAll(".tabs__tab");
const active = document.querySelector(".active_tab");

if (tabs.length > 0 && active) {
  let currentTab = 0;

  const move = (target, ac) => {
    const { offsetLeft, offsetTop, offsetWidth, offsetHeight } = target;
    active.style.left = `${offsetLeft}px`;
    active.style.top = `${offsetTop}px`;
    active.style.width = `${offsetWidth}px`;
    active.style.height = `${offsetHeight}px`;
    currentTab = ac;
  };

  // Detectar cuál tab es el actual en base a URL
  tabs.forEach((tab, index) => {
    if (window.location.pathname === tab.dataset.href) {
      currentTab = index;
    }
  });

  // Posicionar cuadro al cargar
  move(tabs[currentTab], currentTab);

  tabs.forEach((el, index) => {
    el.addEventListener("click", (e) => {
      e.preventDefault(); // Evita navegación inmediata
      move(el, index);    // Mueve el cuadro
      const href = el.dataset.href;
      setTimeout(() => {
        window.location.href = href;
      }, 300); // Tiempo para ver la animación
    });
  });

  window.addEventListener("resize", () => {
    move(tabs[currentTab], currentTab);
  });
}



// Mostrar/Cerrar formulario de contacto
function accionLapiz() {
  document.getElementById('formulario-editar').style.display = 'flex';
}
function cerrarFormulario() {
  document.getElementById('formulario-editar').style.display = 'none';
}

// Descripción
function mostrarFormularioDescripcion() {
  document.getElementById('formulario-añadir-descripcion').style.display = 'flex';
}
function cerrarFormularioDescripcion() {
  document.getElementById('formulario-añadir-descripcion').style.display = 'none';
}
function mostrarFormularioeditarDescripcion() {
  const descripcionActual = document.getElementById('descripcionMostrado').textContent;
  document.getElementById('descripcionEditar').value = descripcionActual;
  document.getElementById('formulario-editar-descripcion').style.display = 'flex';
}
function cerrarFormularioeditarDescripcion() {
  document.getElementById('formulario-editar-descripcion').style.display = 'none';
}

// Ubicacion

function mostrarFormularioUbicacion() {
  document.getElementById('formularioUbicacion').style.display = 'flex';
}

function cerrarFormularioUbicacion() {
  document.getElementById('formularioUbicacion').style.display = 'none';
}

function cerrarFormularioEditarUbicacion() {
  document.getElementById('formularioUbicacionEditar').style.display = 'none';
}

// Experiencia
function mostrarFormularioExperiencia() {
  document.getElementById('formulario-experiencia').style.display = 'flex';
}
function cerrarFormularioExperiencia() {
  document.getElementById('formulario-experiencia').style.display = 'none';
}
function cerrarFormularioEditarExperiencia() {
  document.getElementById('formulario-editar-experiencia').style.display = 'none';
}

// Estudios
function mostrarFormularioEstudios() {
  document.getElementById('formulario-estudios').style.display = 'flex';
}
function cerrarFormularioEstudios() {
  document.getElementById('formulario-estudios').style.display = 'none';
}
function cerrarFormularioEditarEstudios() {
  document.getElementById('formulario-editar-estudios').style.display = 'none';
}

// Idiomas
function cerrarFormularioIdiomas() {
  document.getElementById('formularioIdioma').style.display = 'none';
}

// Aptitudes
function cerrarFormularioAptitudes() {
  document.getElementById('formularioAptitudes').style.display = 'none';
}

// Mostrar imagen de perfil y enviar automáticamente
function mostrarImagen(event) {
  const input = event.target;
  const reader = new FileReader();

  reader.onload = function () {
    const preview = document.getElementById('preview');
    preview.style.backgroundImage = `url(${reader.result})`;
    preview.innerHTML = ''; // Elimina el ícono
  };

  if (input.files[0]) {
    reader.readAsDataURL(input.files[0]);

    setTimeout(() => {
      document.getElementById('formImagen').submit();
    }, 500);
  }
}

// Carrusel de calificaciones
document.addEventListener("DOMContentLoaded", function () {
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


  // Editar experiencia
  const lapizExperiencia = document.getElementById('lapizexperiencia');
  if (lapizExperiencia) {
    lapizExperiencia.addEventListener('click', function () {
      const item = this.closest('.item-experiencia');
      const cargo = item.querySelector('.titulo-experiencia').innerText;
      const empresa = item.querySelector('.empresa').innerText;
      const fechas = item.querySelector('.fechas').innerText;

      const desde = fechas.match(/DESDE: ([^,]*)/)?.[1] || '';
      const hasta = fechas.match(/HASTA: (.*)/)?.[1] || '';

      document.getElementById('editar-cargo').value = cargo;
      document.getElementById('editar-empresa').value = empresa;
      document.getElementById('editar-desde').value = desde;
      document.getElementById('editar-hasta').value = hasta;

      document.getElementById('formulario-editar-experiencia').style.display = 'flex';
    });
  }

  // Editar estudios
  const lapizEstudios = document.getElementById('lapizestudios');
  if (lapizEstudios) {
    lapizEstudios.addEventListener('click', function () {
      const item = this.closest('.item-estudios');
      const titulo = item.querySelector('.titulo-estudios').innerText;
      const lugar = item.querySelector('.lugar').innerText;
      const fecha = item.querySelector('.fecha').innerText;

      const desde = fecha.match(/DESDE: ([^,]*)/)?.[1] || '';
      const hasta = fecha.match(/HASTA: (.*)/)?.[1] || '';

      document.getElementById('editar-titulo').value = titulo;
      document.getElementById('editar-lugar').value = lugar;
      document.getElementById('editar-fechaDesde').value = desde;
      document.getElementById('editar-fechaHasta').value = hasta;

      document.getElementById('formulario-editar-estudios').style.display = 'flex';
    });
  }


  // Mostrar formulario Idioma
  const btnAgregarIdiomas = document.getElementById("agregaridiomas");
  if (btnAgregarIdiomas) {
    btnAgregarIdiomas.addEventListener("click", () => {
      document.getElementById("formularioIdioma").style.display = "flex";
    });
  }

  // Mostrar formulario Aptitudes
  const btnAgregarAptitudes = document.getElementById("agregaraptitudes");
  if (btnAgregarAptitudes) {
    btnAgregarAptitudes.addEventListener("click", () => {
      document.getElementById("formularioAptitudes").style.display = "flex";
    });
  }

const modalEliminar = document.getElementById('modalEliminar');
const textoEliminar = document.getElementById('textoEliminar');
const btnConfirmar = document.getElementById('confirmEliminar');
const btnCancelar = document.getElementById('cancelEliminar');

let formActual = null;

// Abrir modal al hacer clic en botón eliminar
document.querySelectorAll('.btn-eliminar').forEach(btn => {
  btn.addEventListener('click', () => {
    formActual = btn.closest('form');
    textoEliminar.textContent = btn.dataset.texto; // personaliza mensaje
    modalEliminar.classList.remove('hidden');
  });
});

// Confirmar eliminación
btnConfirmar.addEventListener('click', () => {
  if (formActual) formActual.submit();
});

// Cancelar eliminación
btnCancelar.addEventListener('click', () => {
  modalEliminar.classList.add('hidden');
  formActual = null;
});

// Cerrar modal al hacer clic fuera del contenido
modalEliminar.addEventListener('click', (e) => {
  if (e.target === modalEliminar) { // Solo si clic fuera del contenido
    modalEliminar.classList.add('hidden');
    formActual = null;
  }
});



});


// Cerrar formularios al hacer clic fuera
document.addEventListener('mousedown', function (event) {
  const formulariosConfig = [
    { id: 'formulario-editar', contenido: '.formulario-contenido' },
    { id: 'formulario-añadir-descripcion', contenido: '.formulario-contenido-descripcion' },
    { id: 'formulario-editar-descripcion', contenido: '.formulario-contenido-descripcion' },
    { id: 'formulario-experiencia', contenido: '.formulario-experiencia-contenido' },
    { id: 'formulario-editar-experiencia', contenido: '.formulario-experiencia-contenido' },
    { id: 'formulario-estudios', contenido: '.formulario-estudios-contenido' },
    { id: 'formulario-editar-estudios', contenido: '.formulario-estudios-contenido' },
    { id: 'formularioIdioma', contenido: '.formulario-contenido' },
    { id: 'formularioAptitudes', contenido: '.formulario-contenido' },
    { id: 'formularioUbicacion', contenido: '.formulario-ubicacion-contenido' },
    { id: 'formularioUbicacionEditar', contenido: '.formulario-ubicacion-contenido' },
  ];

  formulariosConfig.forEach(({ id, contenido }) => {
    const modal = document.getElementById(id);
    if (modal && modal.style.display === 'flex') {
      const box = modal.querySelector(contenido);
      // si el clic NO fue dentro del contenido, cerrar el modal
      if (box && !box.contains(event.target)) {
        modal.style.display = 'none';
      }
    }
  });
});


// Guardar nuevo barrio FRONTENDDD  -- SOLO VISUAL
function guardarNuevoBarrio() {
  const input = document.getElementById('nuevo-barrio');
  const valor = input.value.trim();
  if (valor === '') return;

  const ubicacionDiv = document.querySelector('.ubicacion');

  // Si ya existe, lo reemplazamos
  let itemUbicacion = ubicacionDiv.querySelector('.item-ubicacion');
  if (!itemUbicacion) {
    itemUbicacion = document.createElement('div');
    itemUbicacion.className = 'item-ubicacion';
    itemUbicacion.innerHTML = `
      <div class="fila-ubicacion">
        <p class="barrio"></p>
        <div class="iconos">
          <i id="lapizubicacion" class="bi bi-pencil-square" onclick="abrirFormularioEditarUbicacion()"></i>
          <i class="bi bi-trash" onclick="eliminarBarrio()"></i>
        </div>
      </div>
    `;
    ubicacionDiv.appendChild(itemUbicacion);
  }

  itemUbicacion.querySelector('.barrio').textContent = valor;
  cerrarFormularioUbicacion();
  document.querySelector('.añadir-ubicacion')?.classList.add('hidden');
}

// Guardar edición de barrio
function guardarEdicionBarrio() {
  const input = document.getElementById('editar-barrio');
  const valor = input.value.trim();
  if (valor === '') return;

  const barrioP = document.querySelector('.item-ubicacion .barrio');
  if (barrioP) barrioP.textContent = valor;

  cerrarFormularioEditarUbicacion();
}

// Abrir formulario editar barrio
function abrirFormularioEditarUbicacion() {
  const barrioP = document.querySelector('.item-ubicacion .barrio');
  if (barrioP) {
    document.getElementById('editar-barrio').value = barrioP.textContent;
    document.getElementById('formularioUbicacionEditar').style.display = 'flex';
  }
}

// Eliminar barrio
function eliminarBarrio() {
  const item = document.querySelector('.item-ubicacion');
  if (item) {
    item.remove();
    document.querySelector('.añadir-ubicacion')?.classList.remove('hidden');
  }
}

// === Mostrar formulario de editar estudios ===
document.getElementById("lapizestudios")?.addEventListener("click", () => {
  document.getElementById("formulario-editar-estudios").style.display = "flex";
});

// === Cerrar formulario de editar estudios ===
function cerrarFormularioEditarEstudios() {
  document.getElementById("formulario-editar-estudios").style.display = "none";
}


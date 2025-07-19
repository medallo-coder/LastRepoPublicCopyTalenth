// Navegación
function activarTab(element) {
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => tab.classList.remove('active'));
  element.classList.add('active');
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

// Carrusel
document.addEventListener("DOMContentLoaded", function () {
  const slider = document.getElementById("slider");
  const arrowButtons = document.querySelectorAll(".arrow-btn");

  function getScrollAmount() {
    return window.innerWidth <= 480 ? 365 : 600;
  }

  arrowButtons[0]?.addEventListener("click", () => {
    slider.scrollBy({
      left: -getScrollAmount(),
      behavior: "smooth"
    });
  });

  arrowButtons[1]?.addEventListener("click", () => {
    slider.scrollBy({
      left: getScrollAmount(),
      behavior: "smooth"
    });
  });

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
});

// Cerrar formularios al hacer clic fuera
document.addEventListener('mousedown', function (event) {
  const excepciones = [
    '.formulario-contenido',
    '.formulario-contenido-descripcion',
    '.formulario-experiencia-contenido',
    '.formulario-editar-experiencia-contenido',
    '.formulario-estudios-contenido',
    '.formulario-editar-estudios-contenido'
  ];

  const formularios = [
    'formulario-editar',
    'formulario-añadir-descripcion',
    'formulario-editar-descripcion',
    'formulario-experiencia',
    'formulario-editar-experiencia',
    'formulario-estudios',
    'formulario-editar-estudios',
    'formularioIdioma',
    'formularioAptitudes'
  ];

  formularios.forEach((id, i) => {
    const modal = document.getElementById(id);
    const selectorContenido = excepciones[i] || '.formulario-contenido';
    if (modal && modal.style.display === 'flex') {
      const contenido = modal.querySelector(selectorContenido);
      if (contenido && !contenido.contains(event.target)) {
        modal.style.display = 'none';
      }
    }
  });
});

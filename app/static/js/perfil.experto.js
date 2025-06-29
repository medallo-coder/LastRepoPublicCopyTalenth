
 //Navegacion
function activarTab(element) {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    element.classList.add('active');
  }

  // Función para abrir el formulario
function accionLapiz() {
    document.getElementById('formulario-editar').style.display = 'flex'; // Muestra el formulario
  }
  
  // Función para cerrar el formulario
  function cerrarFormulario() {
    document.getElementById('formulario-editar').style.display = 'none'; // Oculta el formulario
  }
  

  // Descripcion 

  // Mostrar formulario de añadir descripción
function mostrarFormularioDescripcion() {
  document.getElementById('formulario-añadir-descripcion').style.display = 'flex';
}

// Cerrar formulario de añadir descripción
function cerrarFormularioDescripcion() {
  document.getElementById('formulario-añadir-descripcion').style.display = 'none';
}

// Guardar la descripción y actualizar la interfaz
function guardarDescripcion(event) {
  event.preventDefault();
  const descripcion = document.getElementById('descripcionAñadir').value;

  // Mostrar la descripción guardada
  document.getElementById('descripcionMostrado').textContent = descripcion;

  // Mostrar el bloque de descripción y ocultar el botón de añadir
  document.querySelector('.item-descripcion').style.display = 'block';
  document.querySelector('.titulo-izquierda').style.display = 'block';
  document.getElementById('btnAñadirDescripcion').style.display = 'none';

  // Cerrar el formulario
  cerrarFormularioDescripcion();
}

// Mostrar formulario para editar la descripción
function mostrarFormularioeditarDescripcion() {
  const descripcionActual = document.getElementById('descripcionMostrado').textContent;
  document.getElementById('descripcionEditar').value = descripcionActual;
  document.getElementById('formulario-editar-descripcion').style.display = 'flex';
}

// Guardar cambios de la descripción editada
function guardarEdicionDescripcion(event) {
  event.preventDefault();
  const descripcionEditada = document.getElementById('descripcionEditar').value;
  document.getElementById('descripcionMostrado').textContent = descripcionEditada;
  cerrarFormularioeditarDescripcion();
}

// Cerrar el formulario de edición
function cerrarFormularioeditarDescripcion() {
  document.getElementById('formulario-editar-descripcion').style.display = 'none';
}

  
  // EXPERIENCIA

  function mostrarFormularioExperiencia() {
    document.getElementById('formulario-experiencia').style.display = 'flex';
  }
  
  function cerrarFormularioExperiencia() {
    document.getElementById('formulario-experiencia').style.display = 'none';
  }
  
  
  document.getElementById('lapizexperiencia').addEventListener('click', function () {
    // Obtener los datos actuales
    const item = this.closest('.item-experiencia');
    const cargo = item.querySelector('.rol').innerText;
    const empresa = item.querySelector('.empresa').innerText;
    const fechas = item.querySelector('.fechas').innerText;
    
    // Separar fechas
    const [desde, hasta] = fechas.split(' - ');

    // Llenar los campos del formulario
    document.getElementById('editar-cargo').value = cargo;
    document.getElementById('editar-empresa').value = empresa;
    document.getElementById('editar-desde').value = desde;
    document.getElementById('editar-hasta').value = hasta;

    // Mostrar formulario
    document.getElementById('formulario-editar-experiencia').style.display = 'flex';
  });

  function cerrarFormularioEditarExperiencia() {
    document.getElementById('formulario-editar-experiencia').style.display = 'none';
  }

  // ESTUDIOS 

  
  function mostrarFormularioEstudios() {
    document.getElementById('formulario-estudios').style.display = 'flex';
  }
  
  function cerrarFormularioEstudios() {
    document.getElementById('formulario-estudios').style.display = 'none';
  }
  
  document.getElementById('lapizestudios').addEventListener('click', function () {
    // Obtener los datos actuales
    const item = this.closest('.item-estudios');
    const titulo = item.querySelector('.titulo').innerText;
    const lugar = item.querySelector('.lugar').innerText;
    const fecha = item.querySelector('.fecha').innerText;
    
    // Separar fechas
    const [desde, hasta] = fecha.split(' - ');

    // Llenar los campos del formulario
    document.getElementById('editar-titulo').value = titulo;
    document.getElementById('editar-lugar').value = lugar;
    document.getElementById('editar-fechaDesde').value = desde;
    document.getElementById('editar-fechaHasta').value = hasta;

    // Mostrar formulario
    document.getElementById('formulario-editar-estudios').style.display = 'flex';
  });

  function cerrarFormularioEditarEstudios() {
    document.getElementById('formulario-editar-estudios').style.display = 'none';
  }

  // Idiomas
  const btnAbrir = document.getElementById("agregaridiomas");
  const formulario = document.getElementById("formularioIdioma");
  const btnCancelar = document.getElementById("cancelarFormulario");
  
  // Muestra el formulario cuando se hace clic en el ícono de agregar idioma
  btnAbrir.addEventListener("click", () => {
    formulario.style.display = "flex"; // Muestra el formulario
  });

   // Función para cerrar el formulario idiomas
   function cerrarFormularioIdiomas() {
    document.getElementById('formularioIdioma').style.display = 'none'; // Oculta el formulario
  }
  
   // Mostrar el formulario al hacer clic en el icono "+"
   document.getElementById('agregaraptitudes').addEventListener('click', function () {
    document.getElementById('formularioAptitudes').style.display = 'flex';
  });

  // Función para cerrar el formulario al hacer clic en "Cancelar"
  function cerrarFormularioAptitudes() {
    document.getElementById('formularioAptitudes').style.display = 'none';
  }

  
document.addEventListener("DOMContentLoaded", function () {
  const slider = document.getElementById("slider");
  const arrowButtons = document.querySelectorAll(".arrow-btn");

  // Detectar el ancho de pantalla
  function getScrollAmount() {
    if (window.innerWidth <= 480) {
      return 365; // Desplazamiento más lento (menor) para celulares
    } else {
      return 600; // Normal para pantallas grandes
    }
  }

  arrowButtons[0].addEventListener("click", () => {
    slider.scrollBy({
      left: -getScrollAmount(),
      behavior: "smooth"
    });
  });

  arrowButtons[1].addEventListener("click", () => {
    slider.scrollBy({
      left: getScrollAmount(),
      behavior: "smooth"
    });
  });
});



function mostrarImagen(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const preview = document.getElementById('preview');
      preview.style.backgroundImage = `url('${e.target.result}')`;
      preview.style.backgroundSize = 'cover';
      preview.style.backgroundPosition = 'center';
      preview.innerHTML = ''; // Quitamos el ícono si ya hay imagen
    }
    reader.readAsDataURL(file);
  }
}

function mostrarImagen(event) {
    const input = event.target;
    const reader = new FileReader();

    reader.onload = function() {
      const preview = document.getElementById('preview');
      preview.style.backgroundImage = `url(${reader.result})`;
      preview.innerHTML = ''; // Elimina el ícono
    };

    if (input.files[0]) {
      reader.readAsDataURL(input.files[0]);

      // Enviar formulario automáticamente
      setTimeout(() => {
        document.getElementById('formImagen').submit();
      }, 500);
    }
  }
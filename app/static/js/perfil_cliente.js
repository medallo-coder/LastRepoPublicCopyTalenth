
 //Navegacion
 function activarTab(element) {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    element.classList.add('active');
  }

  
  // Función para abrir el formulario EDITAR CONTACTO
  function accionLapiz() {
    document.getElementById('formulario-editar').style.display = 'flex';
  }

  // Función para cerrar el formulario EDITAR CONTACTO
  function cerrarFormulario() {
    document.getElementById('formulario-editar').style.display = 'none';
  }
 
  // UBICACIÓN - barrio
  function mostrarFormularioUbicacion() {
    document.getElementById('formularioUbicacion').style.display = 'flex';
  }

  function cerrarFormularioUbicacion() {
    document.getElementById('formularioUbicacion').style.display = 'none';
  }

  document.getElementById('lapizubicacion').addEventListener('click', function () {
    const item = this.closest('.item-ubicacion');
    const barrio = item.querySelector('.barrio').innerText;
    document.getElementById('editar-barrio').value = barrio;
    document.getElementById('formularioUbicacionEditar').style.display = 'flex';
  });

  function cerrarFormularioEditarUbicacion() {
    document.getElementById('formularioUbicacionEditar').style.display = 'none';
  }


  // EMPRESA
   // Añadir empresa
  function mostrarFormularioEmpresa() {
    document.getElementById('formulario-empresa').style.display = 'flex';
  }

  function cerrarFormularioEmpresa() {
    document.getElementById('formulario-empresa').style.display = 'none';
  }

  // Editar empresa
  document.getElementById('lapizempresa').addEventListener('click', function () {
    const item = this.closest('.item-empresa');
    const empresa = item.querySelector('.nombre_empresa').innerText;
    document.getElementById('editar-empresa').value = empresa;
    document.getElementById('formulario-editar-empresa').style.display = 'flex';
  });

  function cerrarFormularioEditarEmpresa() {
    document.getElementById('formulario-editar-empresa').style.display = 'none';
  }

  //CALIFICACIONES

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
  
  document.addEventListener('DOMContentLoaded', () => {
    const menuButtons = document.querySelectorAll('.menu-button');
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');
  
    // Agregar el evento de click para cada botón
    menuButtons.forEach((button, index) => {
      const dropdownMenu = dropdownMenus[index];
  
      button.addEventListener('click', (e) => {
        e.stopPropagation(); // Evita que se cierre inmediatamente
        const isVisible = dropdownMenu.style.display === 'block';
        
        // Cerrar todos los menús antes de abrir el que corresponde
        dropdownMenus.forEach((menu) => (menu.style.display = 'none'));
  
        // Mostrar el menú del botón clicado
        dropdownMenu.style.display = isVisible ? 'none' : 'block';
      });
    });
  
    // Cierra el menú si se hace clic fuera de él
    document.addEventListener('click', () => {
      dropdownMenus.forEach((menu) => (menu.style.display = 'none'));
    });
  
    // Evita cierre si se hace clic dentro del menú
    dropdownMenus.forEach((menu) => {
      menu.addEventListener('click', (e) => {
        e.stopPropagation();
      });
    });
  });
  

  
// TARJETAS - DESCRIPCIÓN Y VER MÁS
document.addEventListener('DOMContentLoaded', () => {
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

  document.getElementById('cerrarTarjeta').addEventListener('click', () => {
    document.getElementById('modalTarjeta').classList.add('hidden');
  });
});

//foto 

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
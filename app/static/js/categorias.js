document.querySelectorAll(".menu-button").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation(); // Previene que el evento se propague
      const menu = btn.nextElementSibling;
      document.querySelectorAll(".dropdown-menu").forEach((m) => {
        if (m !== menu) m.classList.add("hidden");
      });
      menu.classList.toggle("hidden");
    });
  });

  // Cierra los menús si se hace clic fuera
  window.addEventListener("click", () => {
    document.querySelectorAll(".dropdown-menu").forEach((menu) => {
      menu.classList.add("hidden");
    });
  });
const btnToggle = document.getElementById('toggleFiltros');
const panel = document.getElementById('panelFiltros');
const contenidoFiltrosMobile = document.getElementById('contenidoFiltrosMobile');

// Crear overlay si no existe
let overlay = document.getElementById('overlayFiltros');
if (!overlay) {
  overlay = document.createElement('div');
  overlay.id = 'overlayFiltros';
  overlay.style.position = 'fixed';
  overlay.style.top = '0';
  overlay.style.left = '0';
  overlay.style.width = '100%';
  overlay.style.height = '100%';
  overlay.style.background = 'rgba(0,0,0,0.4)'; // negro claro
  overlay.style.zIndex = '40'; // menos que el panel (50)
  overlay.style.display = 'none';
  document.body.appendChild(overlay);
}

btnToggle.addEventListener('click', () => {
  // Clonar filtros
  const filtros = document.getElementById('cuadroFiltros').cloneNode(true);
  filtros.classList.remove('hidden');

  // Limpiar y agregar al panel móvil
  contenidoFiltrosMobile.innerHTML = '';
  contenidoFiltrosMobile.appendChild(filtros);

  // Mostrar panel y overlay
  panel.classList.remove('hidden');
  overlay.style.display = 'block';
  document.body.style.overflow = 'hidden';

  // 🔹 Asignar evento a la X dentro del panel móvil
  const cerrarMobile = panel.querySelector('#cerrarFiltros');
  if (cerrarMobile) {
    cerrarMobile.onclick = cerrarPanel;
  }

  // 🔹 Cerrar panel al hacer clic en el overlay
  overlay.onclick = cerrarPanel;

  // 🔹 Eventos internos (categorías/subcategorías)
  const toggleCategoriasMobile = filtros.querySelector("#toggleCategorias");
  const categoriasMobile = filtros.querySelector("#categorias");

  if (toggleCategoriasMobile) {
    toggleCategoriasMobile.addEventListener("click", () => {
      categoriasMobile.classList.toggle("hidden");
    });
  }

  const toggleSubcategoriasMobile = filtros.querySelector("#toggleSubcategorias");
  const subcategoriasMobile = filtros.querySelector("#subcategorias");

  if (toggleSubcategoriasMobile) {
    toggleSubcategoriasMobile.addEventListener("click", () => {
      subcategoriasMobile.classList.toggle("hidden");
    });
  }
});

// Función para cerrar panel y overlay
function cerrarPanel() {
  panel.classList.add('hidden');
  overlay.style.display = 'none';
  document.body.style.overflow = '';
}


    // TARJETAS - DESCRIPCIÓN Y VER MÁS
document.addEventListener('DOMContentLoaded', () => {
  const tarjetas = document.querySelectorAll('.tarjeta');

  // Función que devuelve el límite de caracteres según el tamaño de pantalla
   function getDescripcionLimit() {
    if (window.innerWidth <= 480) return 25;       // Celulares
    if (window.innerWidth <= 768) return 35;       // Tablets vertical
    if (window.innerWidth <= 1024) return 55;      // Tablets horizontal
    if (window.innerWidth <= 1366) return 35;   
    if (window.innerWidth <= 1600) return 78;     // Laptops grandes
    return 125;                                    // Pantallas muy grandes
  }


  // Función para aplicar el recorte dinámico a TODAS las tarjetas
  function aplicarDescripcionResponsive() {
    const limite = getDescripcionLimit();

    tarjetas.forEach(tarjeta => {
      const descripcionElem = tarjeta.querySelector('.descripcion');
      const verMasBtn = tarjeta.querySelector('.ver-mas');

      // Guardar la descripción completa si aún no existe en data
      if (!descripcionElem.dataset.completa) {
        descripcionElem.dataset.completa = descripcionElem.textContent.trim();
      }

      const descripcionCompleta = descripcionElem.dataset.completa;

      if (descripcionCompleta.length > limite) {
        descripcionElem.textContent = descripcionCompleta.substring(0, limite) + '...';
        verMasBtn.classList.add('visible');
      } else {
        descripcionElem.textContent = descripcionCompleta;
        verMasBtn.classList.remove('visible');
      }

      // Evento para abrir el modal con la descripción completa
      verMasBtn.onclick = () => {
  const tarjetaClonada = tarjeta.cloneNode(true);

  // ✅ Forzar el layout en el modal
  tarjetaClonada.classList.remove("flex-col", "text-center", "items-center", "lg:items-start");
  tarjetaClonada.classList.add("flex-row", "items-center", "gap-4", "text-left");

  // Mostrar el texto completo en el modal
  const descripcionModal = tarjetaClonada.querySelector('.descripcion');
  descripcionModal.textContent = descripcionCompleta;
  descripcionModal.classList.add('descripcion-modal');

  // Eliminar el botón "Ver más" en el modal
  const btnModal = tarjetaClonada.querySelector('.ver-mas');
  if (btnModal) btnModal.remove();

  // Eliminar menú de 3 puntos en el modal
  const menuContainer = tarjetaClonada.querySelector('.menu-button-container');
  if (menuContainer) menuContainer.remove();

  // Agregar el contenido al modal
  const contenedorModal = document.getElementById('contenidoTarjeta');
  contenedorModal.innerHTML = '';
  contenedorModal.appendChild(tarjetaClonada);

  // Mostrar modal
  document.getElementById('modalTarjeta').classList.remove('hidden');

  // Forzar que la imagen del modal sea más grande
const img = tarjetaClonada.querySelector("img, i.bi-person-circle");
if (img && img.tagName === "IMG") {
  img.style.width = "125px";
  img.style.height = "120px";
  img.style.borderRadius = "50%"; // O "50%" si quieres círculo
}

};

    });
  }

  // Ejecutar al cargar la página
  aplicarDescripcionResponsive();

  // Reaplicar cuando cambia el tamaño de la ventana
  window.addEventListener('resize', aplicarDescripcionResponsive);

  // Cerrar el modal al hacer clic en la "X"
  const cerrarModal = document.getElementById('cerrarTarjeta');
  cerrarModal.addEventListener('click', () => {
    document.getElementById('modalTarjeta').classList.add('hidden');
  });

  // --- Cerrar modal al hacer clic fuera del contenido ---
const modalTarjeta = document.getElementById('modalTarjeta');
modalTarjeta.addEventListener('click', (e) => {
  if (e.target === modalTarjeta) {  
    modalTarjeta.classList.add('hidden');
  }
});

});



    // Botón para mostrar/ocultar categorías
document.getElementById("toggleCategorias").addEventListener("click", function () {
  document.getElementById("categorias").classList.toggle("hidden");
});

// Botón para mostrar/ocultar subcategorías
document.getElementById("toggleSubcategorias").addEventListener("click", function () {
  document.getElementById("subcategorias").classList.toggle("hidden");
});

// Datos de subcategorías por categoría
const subcategoriasData = {
  reparacion: ['Plomería', 'Electricidad', 'Carpintería', 'Pintura y decoración', 'Reparaciones generales', 'Cerrajería', , 'Reparación de electrodomésticos' , 'Técnico en computadora/celulares'],
  cuidado: ['Cuidado de adultos mayores', 'Cuidado de niños', 'Asistencia personal', 'Cuidado de mascotas' , 'Paseo de mascotas' , 'Baño para mascotas'],
  educativos: ['Clases particulares', 'Coaching', 'Enseñanza de idiomas', 'Formación en habilidades digitales', 'Clases de música' , 'Tutorías'],
  construccion: ['Albañilería', 'Instalación de pisos', 'Remodelación de cocinas', 'Reparación de techos' , 'Diseño de interiores' , 'Impermeabilización'],
  hogar: ['Aseo doméstico', 'Jardinería', 'Organización de espacios', 'Desinfección' , 'Fumigación'],
  creativos: ['Fotografía', 'Redacción y traducción', 'Producción de video'],
  transporte: ['Mudanzas', 'Reparto/domicilios'],
  eventos: ['Organización de eventos', 'Decoración para fiestas' , 'Chef' , 'Repostería personalizada'],
  salud: ['Entrenador/a personal' , 'Masajes' , 'Estética'],

};

// Función para cargar subcategorías según la categoría seleccionada
function mostrarSubcategorias(categoria) {
  const contenedor = document.getElementById("subcategorias");
  contenedor.innerHTML = "";

  if (!categoria || !subcategoriasData[categoria]) return;

  subcategoriasData[categoria].forEach(sub => {
    const label = document.createElement("label");
    label.className = "flex items-center space-x-2 cursor-pointer";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "w-5 h-5";
    const span = document.createElement("span");
    span.className = "text-gray-500";
    span.textContent = sub;

    label.appendChild(checkbox);
    label.appendChild(span);
    contenedor.appendChild(label);
  });
}

// Cuando se selecciona una categoría
const radios = document.querySelectorAll(".category-radio");
radios.forEach(radio => {
  radio.addEventListener("change", function () {
    const categoriaSeleccionada = this.closest(".category").getAttribute("data-category");

    if (this.checked) {
      mostrarSubcategorias(categoriaSeleccionada);
      document.getElementById("subcategoriasSection").classList.remove("hidden");
      document.getElementById("subcategorias").classList.remove("hidden");
    }
  });
});

// Si se deselecciona (con otro click), se ocultan subcategorías
document.getElementById("categorias").addEventListener("click", function (e) {
  const target = e.target;
  if (target.type === "radio") {
    // Delay para esperar al cambio de estado
    setTimeout(() => {
      const seleccionado = document.querySelector(".category-radio:checked");
      if (!seleccionado) {
        document.getElementById("subcategoriasSection").classList.add("hidden");
        document.getElementById("subcategorias").classList.add("hidden");
        document.getElementById("subcategorias").innerHTML = "";
      }
    }, 100);
  }
});

document.querySelectorAll(".category-radio").forEach(radio => {
  radio.addEventListener("change", function () {
    const categoria = this.closest(".category").dataset.category;

    if (categoria === "todas") {
      document.getElementById("subcategoriasSection").classList.add("hidden");
      document.getElementById("subcategorias").classList.add("hidden");
      document.getElementById("subcategorias").innerHTML = "";
    }
  });
});

//validar que el rango maximo no sea menor al minimo
const minInput = document.getElementById('minPrice');
  const maxInput = document.getElementById('maxPrice');

  minInput.addEventListener('input', () => {
    const minValue = parseInt(minInput.value, 10);
    if (!isNaN(minValue)) {
      maxInput.min = minValue;
      if (parseInt(maxInput.value, 10) < minValue) {
        maxInput.value = minValue; // Opcional: ajustar automáticamente el valor
      }
    }
  });


// Función para actualizar el cuadro de categoría
function actualizarCuadroServicio(categoria = 'Todas') {
  document.getElementById('categoriaTexto').textContent = 'Categoría';
  document.getElementById('subcategoriaTexto').textContent = categoria;
}

// Mostrar por defecto "Todas"
actualizarCuadroServicio('Todas');

// Cuando se selecciona una categoría
radios.forEach(radio => {
  radio.addEventListener("change", function () {
    const categoriaSeleccionada = this.closest(".category").getAttribute("data-category");
    if (this.checked) {
      const nombreCategoria = this.closest(".category").querySelector("span").textContent.trim();
      actualizarCuadroServicio(nombreCategoria);
    }
  });
});


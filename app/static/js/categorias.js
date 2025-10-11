// =======================
//  MENÚS DESPLEGABLES
// =======================
document.querySelectorAll(".menu-button").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    const menu = btn.nextElementSibling;
    document.querySelectorAll(".dropdown-menu").forEach((m) => {
      if (m !== menu) m.classList.add("hidden");
    });
    menu.classList.toggle("hidden");
  });
});

// Cerrar menús al hacer clic fuera
window.addEventListener("click", () => {
  document.querySelectorAll(".dropdown-menu").forEach((menu) => {
    menu.classList.add("hidden");
  });
});

// =======================
//  PANEL DE FILTROS RESPONSIVE (MÓVIL)
// =======================
const btnToggle = document.getElementById("toggleFiltros");
const panel = document.getElementById("panelFiltros");
const contenidoFiltrosMobile = document.getElementById("contenidoFiltrosMobile");

// Crear overlay si no existe
let overlay = document.getElementById("overlayFiltros");
if (!overlay) {
  overlay = document.createElement("div");
  overlay.id = "overlayFiltros";
  overlay.style.position = "fixed";
  overlay.style.top = "0";
  overlay.style.left = "0";
  overlay.style.width = "100%";
  overlay.style.height = "100%";
  overlay.style.background = "rgba(0,0,0,0.4)";
  overlay.style.zIndex = "40";
  overlay.style.display = "none";
  document.body.appendChild(overlay);
}

// Abrir panel móvil
btnToggle.addEventListener("click", () => {
  const filtrosOriginal = document.getElementById("cuadroFiltros");

  // Clonar filtros del panel original
  const filtrosClon = filtrosOriginal.cloneNode(true);
  filtrosClon.classList.remove("hidden");

  // Limpiar y añadir al contenedor móvil
  contenidoFiltrosMobile.innerHTML = "";
  contenidoFiltrosMobile.appendChild(filtrosClon);

  // Mostrar panel y overlay
  panel.classList.remove("hidden");
  overlay.style.display = "block";
  document.body.style.overflow = "hidden";

  // Cerrar panel (botón X o clic fuera)
  const cerrarMobile = panel.querySelector("#cerrarFiltros");
  if (cerrarMobile) cerrarMobile.onclick = cerrarPanel;
  overlay.onclick = cerrarPanel;

  // Reasignar eventos internos al contenido clonado
  reactivarEventosFiltros(filtrosClon);
});

function cerrarPanel() {
  panel.classList.add("hidden");
  overlay.style.display = "none";
  document.body.style.overflow = "";
}

// =======================
//  FUNCIONES AUXILIARES
// =======================
function reactivarEventosFiltros(contenedor) {
  const toggleCategorias = contenedor.querySelector("#toggleCategorias");
  const categorias = contenedor.querySelector("#categorias");
  const toggleSubcategorias = contenedor.querySelector("#toggleSubcategorias");
  const subcategorias = contenedor.querySelector("#subcategorias");

  // Mostrar/ocultar secciones
  if (toggleCategorias && categorias) {
    toggleCategorias.addEventListener("click", () => {
      categorias.classList.toggle("hidden");
    });
  }
  if (toggleSubcategorias && subcategorias) {
    toggleSubcategorias.addEventListener("click", () => {
      subcategorias.classList.toggle("hidden");
    });
  }

  // Reasignar radios para actualizar cuadro de servicio
  const radios = contenedor.querySelectorAll(".category-radio");
  radios.forEach((radio) => {
    radio.addEventListener("change", function () {
      const categoriaSeleccionada = this.closest(".category")?.dataset.category;
      const nombreCategoria = this.closest(".category")?.querySelector("span")?.textContent.trim() || "Todas";
      if (this.checked) {
        actualizarCuadroServicio(nombreCategoria);
      }
    });
  });

    // --- 🔄 Cargar subcategorías dinámicamente ---
  radios.forEach((radio) => {
    radio.addEventListener("change", async function () {
      const categoriaId = this.value;

      // Contenedor donde se mostrarán las subcategorías
      const subcategoriasSection = contenedor.querySelector("#subcategoriasSection");
      const subcategoriasDiv = contenedor.querySelector("#subcategorias");

      if (!subcategoriasSection || !subcategoriasDiv) return;

      // Si no hay categoría seleccionada (todas), ocultar subcategorías
      if (!categoriaId) {
        subcategoriasSection.classList.add("hidden");
        subcategoriasDiv.innerHTML = "";
        return;
      }

      try {
        // 🔹 Petición al backend para obtener subcategorías
        const response = await fetch(`/subcategorias/${categoriaId}`);
        if (!response.ok) throw new Error("Error al cargar subcategorías");

        const data = await response.json();
        subcategoriasDiv.innerHTML = "";

        // Si hay subcategorías, mostrarlas
        if (data.length > 0) {
          subcategoriasSection.classList.remove("hidden");
          subcategoriasDiv.classList.remove("hidden");

          data.forEach((sub) => {
            const label = document.createElement("label");
            label.className = "flex items-center space-x-2 cursor-pointer";
            label.innerHTML = `
              <input type="radio" name="subcategoria_id" value="${sub.id}" class="subcat-radio" />
              <span class="text-[#666666] text-base">${sub.nombre}</span>
            `;
            subcategoriasDiv.appendChild(label);
          });
        } else {
          subcategoriasSection.classList.add("hidden");
        }
      } catch (error) {
        console.error("❌ Error al obtener subcategorías:", error);
      }
    });
  });

}

// =======================
//  BOTONES PRINCIPALES
// =======================
document.getElementById("toggleCategorias").addEventListener("click", () => {
  document.getElementById("categorias").classList.toggle("hidden");
});

document.getElementById("toggleSubcategorias").addEventListener("click", () => {
  document.getElementById("subcategorias").classList.toggle("hidden");
});



// =======================
//  ACTUALIZAR CUADRO SUPERIOR DE SERVICIO
// =======================
function actualizarCuadroServicio(categoria = "Todas") {
  const categoriaTexto = document.getElementById("categoriaTexto");
  const subcategoriaTexto = document.getElementById("subcategoriaTexto");

  if (categoriaTexto && subcategoriaTexto) {
    categoriaTexto.textContent = "Categoría";
    subcategoriaTexto.textContent = categoria;
  } else {
    console.warn("⚠️ No se encontró el cuadro de servicio (categoriaTexto o subcategoriaTexto).");
  }
}


// Mostrar “Todas” por defecto
actualizarCuadroServicio("Todas");

// =======================
//  RADIOS EN PANEL NORMAL
// =======================
const radios = document.querySelectorAll(".category-radio");
radios.forEach((radio) => {
  radio.addEventListener("change", function () {
    const categoriaSeleccionada = this.closest(".category")?.dataset.category;
    if (this.checked) {
      const nombreCategoria = this.closest(".category")?.querySelector("span")?.textContent.trim() || "Todas";
      actualizarCuadroServicio(nombreCategoria);
    }
  });
});

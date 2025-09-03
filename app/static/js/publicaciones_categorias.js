document.addEventListener("DOMContentLoaded", function () {
  const categoriaRadios = document.querySelectorAll(".category");
  const subcategoriasDiv = document.getElementById("subcategorias");
  const subcategoriasSection = document.getElementById("subcategoriasSection");
  const filtroForm = document.getElementById("filtroForm");

  const cuadro = document.getElementById("cuadroServicio");
  const categoriaTexto = document.getElementById("categoriaTexto");

  // Detectar categoría ya seleccionada al cargar la página (desde URL)
  const urlParams = new URLSearchParams(window.location.search);
  const categoriaIdInicial = urlParams.get("categoria_id");
  const subcategoriaIdInicial = urlParams.get("subcategoria_id");

  if (categoriaIdInicial) {
    cargarSubcategorias(categoriaIdInicial, subcategoriaIdInicial);
    // Mostrar nombre de categoría si ya viene seleccionado al cargar
    const categoriaLabel = document.querySelector(`.category[data-categoria-id="${categoriaIdInicial}"]`);
    if (categoriaLabel) {
      cuadro.classList.remove("hidden");
      categoriaTexto.textContent = categoriaLabel.textContent.trim();
    }
  }

  // Escucha de clics en los radios de categoría
  categoriaRadios.forEach(label => {
    label.addEventListener("click", function () {
      const categoriaId = this.getAttribute("data-categoria-id");

      if (!categoriaId) {
        subcategoriasSection.classList.add("hidden");
        subcategoriasDiv.innerHTML = "";

        // Desmarcar subcategorías
        const subcatInputs = document.querySelectorAll(".subcategory-radio");
        subcatInputs.forEach(input => input.checked = false);

        // Ocultar cuadro y texto de categoría
        cuadro.classList.add("hidden");
        categoriaTexto.textContent = "";

        filtroForm.submit();
        return;
      }

      // Mostrar nombre de la categoría seleccionada en el cuadro
      cuadro.classList.remove("hidden");
      categoriaTexto.textContent = this.textContent.trim();

      // Cargar subcategorías dinámicamente
      cargarSubcategorias(categoriaId);
    });
  });

  // Función para cargar subcategorías
  function cargarSubcategorias(categoriaId, subcatSeleccionada = null) {
    fetch(`/subcategorias/${categoriaId}`)
      .then(res => res.json())
      .then(data => {
        if (!data.length) {
          subcategoriasSection.classList.add("hidden");
          subcategoriasDiv.innerHTML = "";
          filtroForm.submit();
          return;
        }

        subcategoriasSection.classList.remove("hidden");
        subcategoriasDiv.classList.remove("hidden");
        subcategoriasDiv.innerHTML = "";

        data.forEach(sub => {
          const label = document.createElement("label");
          label.className = "flex items-center space-x-2 cursor-pointer subcategory";
          label.innerHTML = `
            <input type="radio" name="subcategoria_id" class="subcategory-radio" value="${sub.id}" ${
              subcatSeleccionada == sub.id ? "checked" : ""
            } />
            <span class="text-[#666666] text-base">${sub.nombre}</span>
          `;
          subcategoriasDiv.appendChild(label);
        });

        // Escuchar selección en subcategorías
        const subcatRadios = subcategoriasDiv.querySelectorAll(".subcategory-radio");
        subcatRadios.forEach(input => {
          input.addEventListener("change", function () {
            filtroForm.submit();
          });
        });
      })
      .catch(err => {
        console.error("Error al obtener subcategorías:", err);
      });
  }

  // Función para cerrar el menú (desde la X)
  window.cerrarMenu = function (elemento) {
    const menu = elemento.closest(".dropdown-menu");
    if (menu) {
      menu.classList.add("hidden");
    }
  };
});// --- Lógica para las tarjetas y modal "Ver más" ---
// --- Lógica para las tarjetas y modal "Ver más" ---
document.addEventListener("DOMContentLoaded", () => {
  const tarjetas = document.querySelectorAll(".tarjeta, .card-tarjeta");
  const modalTarjeta = document.getElementById("modalTarjeta");
  const contenidoTarjeta = document.getElementById("contenidoTarjeta");
  const cerrarTarjetaBtn = document.getElementById("cerrarTarjeta");

  tarjetas.forEach((tarjeta) => {
    const descripcionElem = tarjeta.querySelector(".descripcion");
    const verMasBtn = tarjeta.querySelector(".ver-mas");

    if (!verMasBtn || !descripcionElem) return;

    const textoOriginal = descripcionElem.textContent.trim();

    // Si la descripción es larga, mostrar resumen en la tarjeta
    if (textoOriginal.length > 70) {
      descripcionElem.setAttribute("data-texto-completo", textoOriginal); // 🔑 Guardar el texto real
      descripcionElem.textContent = textoOriginal.substring(0, 70) + "...";
      verMasBtn.classList.remove("hidden");

      verMasBtn.addEventListener("click", () => {
        const tarjetaClonada = tarjeta.cloneNode(true);

        // Restaurar descripción completa en el modal
        const descripcionClon = tarjetaClonada.querySelector(".descripcion");
        if (descripcionClon) {
          const textoCompleto = descripcionElem.getAttribute("data-texto-completo") || textoOriginal;
          descripcionClon.textContent = textoCompleto;
          descripcionClon.classList.remove("h-[60px]", "overflow-hidden");
          descripcionClon.classList.add("h-[200px]", "overflow-y-auto");

          descripcionClon.classList.add("descripcion-modal");
        }

        // Quitar botón "Ver más" y menú
        const verMasClon = tarjetaClonada.querySelector(".ver-mas");
        if (verMasClon) verMasClon.remove();

        const menuClon = tarjetaClonada.querySelector(".menu-button-container");
        if (menuClon) menuClon.remove();

        // Aplicar clase modal
        tarjetaClonada.classList.add("card-tarjeta");

        // Insertar en el modal
        contenidoTarjeta.innerHTML = "";
        contenidoTarjeta.appendChild(tarjetaClonada);

        modalTarjeta.classList.remove("hidden");
      });
    } else {
      verMasBtn.classList.add("hidden");
    }
  });

  // Cerrar modal con botón
  if (cerrarTarjetaBtn) {
    cerrarTarjetaBtn.addEventListener("click", () => {
      modalTarjeta.classList.add("hidden");
      contenidoTarjeta.innerHTML = "";
    });
  }

  // Cerrar modal al hacer clic fuera
  if (modalTarjeta) {
    modalTarjeta.addEventListener("click", (e) => {
      if (e.target === modalTarjeta) {
        modalTarjeta.classList.add("hidden");
        contenidoTarjeta.innerHTML = "";
      }
    });
  }
});

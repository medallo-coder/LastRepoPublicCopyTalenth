document.addEventListener("DOMContentLoaded", () => {
  const categoriaSelect = document.getElementById("categoria");
  const subcategoriaSelect = document.getElementById("subcategoria");
  const formularioModal = document.getElementById("formularioModal");
  const cerrarFormularioBtn = document.getElementById("cerrarFormulario");
  const cancelarFormularioBtn = document.getElementById("cancelarFormulario");

  const subcategoriasDataEl = document.getElementById("data-subcategorias");
  let subcategoriasData = [];
  try {
    subcategoriasData = JSON.parse(subcategoriasDataEl?.textContent || "[]");
  } catch {}

  function filtrarSubcategorias(categoriaId, selectDestino, subcategoriaSeleccionada = null) {
    selectDestino.innerHTML = '<option value="" disabled selected hidden>Selecciona una subcategoría</option>';
    subcategoriasData.forEach(sub => {
      if (sub.categoria_id == categoriaId) {
        const option = document.createElement("option");
        option.value = sub.subcategoria_id;
        option.textContent = sub.nombre_subcategoria;
        if (String(sub.subcategoria_id) === String(subcategoriaSeleccionada)) {
          option.selected = true;
        }
        selectDestino.appendChild(option);
      }
    });
  }

  if (categoriaSelect) {
    categoriaSelect.addEventListener("change", () => {
      const categoriaId = categoriaSelect.value;
      filtrarSubcategorias(categoriaId, subcategoriaSelect);
    });
  }

  cerrarFormularioBtn?.addEventListener("click", () => {
    formularioModal.classList.add("hidden");
  });

  cancelarFormularioBtn?.addEventListener("click", () => {
    formularioModal.classList.add("hidden");
  });

  window.abrirFormularioExperiencia = function () {
    formularioModal.classList.remove("hidden");
  };

  const publicacionesScript = document.getElementById("datos-publicaciones");
  if (publicacionesScript) {
    try {
      const publicaciones = JSON.parse(publicacionesScript.textContent.trim());
      const nombreUsuario = document.getElementById("nombre-usuario")?.textContent || "Usuario";
      publicaciones.forEach(pub => {
        agregarTarjetaAlSlider({
          publicacion_id: pub.publicacion_id,
          nombre_usuario: nombreUsuario,
          titulo: pub.titulo,
          precio: pub.precio,
          descripcion: pub.descripcion_publicacion,
          foto: pub.foto || "default.png"
        });
      });
    } catch (err) {
      console.error("Error cargando tarjetas:", err);
    }
  }

  function agregarTarjetaAlSlider(datos) {
    const contenedor = document.getElementById("slider");
    const nuevaCard = document.createElement("div");
    nuevaCard.className = "card-tarjeta";
    nuevaCard.dataset.publicacionId = datos.publicacion_id;

    nuevaCard.innerHTML = `
      <div class="image-price-container">
        <img src="/static/uploads/${datos.foto}" alt="Foto" />
        <p class="price">COP ${datos.precio}/h</p>
      </div>
      <div class="card-content">
        <div class="header">
          <h3 class="nombre">${datos.nombre_usuario}</h3>
          <div class="menu-button-container">
            <button class="menu-button">
              <i class="bi bi-three-dots"></i>
            </button>
            <div class="menu-completo dropdown-menu">
              <button class="cerrar-menu">✕</button>
              <button onclick="abrirEditarModalFromData(${datos.publicacion_id})">
                <i class="bi bi-pencil-square"></i><span>Editar</span>              <button onclick="abrirEditarModal(
                ${datos.publicacion_id}, 
                \`${datos.titulo.replace(/`/g, "\\`")}\`, 
                '', '', 
                ${datos.precio}, 
                \`${datos.descripcion.replace(/`/g, "\\`")}\`
              )">
                <i class="bi bi-pencil-square"></i><span>Editar</span>
              </button>
              <button class="eliminar-btn" onclick="eliminarPublicacion(${datos.publicacion_id})">
                <i class="bi bi-trash"></i><span>Eliminar</span>
              </button>
            </div>
          </div>
          <div class="estrellasTarjetas">
            <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i>
            <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i>
            <i class="bi bi-star-fill"></i>
          </div>
          <p class="profesion"><strong>${datos.titulo}</strong></p>
          <p class="descripcion-titulo">Descripción:</p>
          <p class="descripcion descripcion-texto">${datos.descripcion}</p>
          <button class="ver-mas hidden">Ver más</button>
        </div>
      </div>
    `;

    contenedor.insertBefore(nuevaCard, document.querySelector(".add-card") || null);

    const newMenuButton = nuevaCard.querySelector(".menu-button");
    const newDropdownMenu = nuevaCard.querySelector(".dropdown-menu");

    newMenuButton.addEventListener("click", (e) => {
      e.stopPropagation();
      const isVisible = newDropdownMenu.style.display === "block";
      document.querySelectorAll(".dropdown-menu").forEach(menu => menu.style.display = "none");
      newDropdownMenu.style.display = isVisible ? "none" : "block";
    });

    newDropdownMenu.addEventListener("click", e => e.stopPropagation());
    newDropdownMenu.querySelector(".cerrar-menu").addEventListener("click", e => {
      e.stopPropagation();
      newDropdownMenu.style.display = "none";
    });
  }

  // Modal de editar
  window.abrirEditarModal = function (id, titulo, categoria, subcategoria, precio, descripcion) {
    const modal = document.getElementById("formularioEditarModal");
    modal.classList.remove("hidden");
    document.getElementById("editar-publicacion-id").value = id;
    document.getElementById("editar-titulo").value = titulo;
    document.getElementById("editar-categoria").value = categoria;
    filtrarSubcategorias(categoria, document.getElementById("editar-subcategoria"), subcategoria);
    document.getElementById("editar-precio").value = precio;
    document.getElementById("editar-descripcion").value = descripcion;
  };

  document.getElementById("cerrarEditarFormulario")?.addEventListener("click", () => {
    document.getElementById("formularioEditarModal").classList.add("hidden");
  });

  document.getElementById("cancelarEditar")?.addEventListener("click", () => {
    document.getElementById("formularioEditarModal").classList.add("hidden");
  });

  window.eliminarPublicacion = function (id) {
    if (confirm("¿Seguro que deseas eliminar esta publicación?")) {
      window.location.href = `/mis-publicaciones/eliminar/${id}`;
    }
  };
});

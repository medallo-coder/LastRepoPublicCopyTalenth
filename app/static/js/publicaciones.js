document.addEventListener("DOMContentLoaded", () => {
  const categoriaSelect = document.getElementById("categoria");
  const subcategoriaSelect = document.getElementById("subcategoria");
  const formulario = document.getElementById("formulario-publicacion");
  const formularioModal = document.getElementById("formularioModal");
  const cerrarFormularioBtn = document.getElementById("cerrarFormulario");
  const cancelarFormularioBtn = document.getElementById("cancelarFormulario");
  const publicacionesScript = document.getElementById("datos-publicaciones");

   // ====== Datos de subcategorías desde el backend ======
const subcategoriasDataEl = document.getElementById("data-subcategorias");
let subcategoriasData = [];

try {
  subcategoriasData = JSON.parse(subcategoriasDataEl?.textContent || "[]");
} catch (e) {
  console.error("❌ Error al parsear subcategorías:", e);
}

  // ====== Datos de subcategorías desde el backend ======
function filtrarSubcategorias(categoriaId, selectDestino, subcategoriaSeleccionada = null) {
  selectDestino.innerHTML = '<option value="" disabled selected hidden>Selecciona una subcategoría</option>';

  let subcatExiste = false;

  subcategoriasData.forEach(sub => {
    if (sub.categoria_id == categoriaId) {
      const option = document.createElement("option");
      option.value = sub.subcategoria_id;
      option.textContent = sub.nombre_subcategoria;

      if (String(sub.subcategoria_id) === String(subcategoriaSeleccionada)) {
        option.selected = true;
        subcatExiste = true;
      }

      selectDestino.appendChild(option);
    }
  });

  if (!subcatExiste && subcategoriaSeleccionada !== null) {
    setTimeout(() => {
      selectDestino.value = String(subcategoriaSeleccionada);
    }, 0);
  }
}


  categoriaSelect.addEventListener("change", () => {
    const categoriaId = categoriaSelect.value;
    subcategoriaSelect.innerHTML = '<option value="">-- Selecciona una subcategoría --</option>';
    subcategoriasData.forEach(sub => {
      if (sub.categoria_id == categoriaId) {
        const option = document.createElement("option");
        option.value = sub.subcategoria_id;
        option.textContent = sub.nombre_subcategoria;
        subcategoriaSelect.appendChild(option);
      }
    });
  });

  subcategoriaSelect.addEventListener("change", () => {
    const subcatSelected = subcategoriaSelect.options[subcategoriaSelect.selectedIndex];
    if (subcatSelected && subcatSelected.dataset.categoria) {
      const categoriaId = subcatSelected.dataset.categoria;
      categoriaSelect.value = categoriaId;
      categoriaSelect.dispatchEvent(new Event("change"));
    }
  });

  formulario.addEventListener("submit", function (e) {
    e.preventDefault();

    const datos = {
      titulo: document.getElementById("titulo").value,
      categoria: document.getElementById("categoria").value,
      subcategoria: document.getElementById("subcategoria").value,
      precio: document.getElementById("precio").value,
      descripcion: document.getElementById("descripcion").value
    };

    fetch("/publicaciones", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert("✅ Publicación creada con éxito.");
        agregarTarjetaAlSlider(data.data);
        verificarLimitePublicaciones();
        formulario.reset();
        formularioModal.classList.add("hidden");
      } else {
        alert("❌ Error: " + data.message);
      }
    })
    .catch(error => {
      alert("❌ Ocurrió un error: " + error.message);
    });
  });

  cerrarFormularioBtn.addEventListener("click", () => {
    formularioModal.classList.add("hidden");
  });

  cancelarFormularioBtn.addEventListener("click", () => {
    formularioModal.classList.add("hidden");
  });

  window.abrirFormularioExperiencia = function () {
    formularioModal.classList.remove("hidden");
  };

  if (publicacionesScript) {
    const publicaciones = JSON.parse(publicacionesScript.textContent);
    const nombreUsuario = document.getElementById("nombre-usuario")?.textContent || "Usuario";

    publicaciones.forEach(pub => {
      agregarTarjetaAlSlider({
        publicacion_id: pub.publicacion_id,
        nombre_usuario: nombreUsuario,
        titulo: pub.titulo,
        precio: pub.precio,
        descripcion: pub.descripcion_publicacion,
        foto: pub.foto || "default.png",
        categoria: pub.categoria_id,
        subcategoria: pub.subcategoria_id
      });
    });

      // 👇 Aquí ocultamos el botón si ya hay 3 publicaciones
    if (publicaciones.length >= 3) {
      const botonAdd = document.querySelector(".add-card");
      if (botonAdd) botonAdd.style.display = "none";
    }
  }
  

  // ====== Función para crear la tarjeta de publicación y asignar eventos ======
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
              <button><i class="bi bi-pencil-square"></i><span>Editar</span></button>
              <button><i class="bi bi-megaphone"></i><span>Promocionar</span></button>
              <button class="eliminar-btn"><i class="bi bi-trash"></i><span>Eliminar</span></button>
            </div>
          </div>
        </div>
        <div class="estrellasTarjetas">
          <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i>
          <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i>
          <i class="bi bi-star-fill"></i>
        </div>
        <p class="profesion"><strong>${datos.titulo}</strong> </p>
        <p class="descripcion-titulo">Descripción:</p>
        <p class="descripcion descripcion-texto">${datos.descripcion}</p>
        <button class="ver-mas hidden">Ver más</button>
      </div>
    `;

    contenedor.insertBefore(nuevaCard, document.querySelector(".add-card"));

    const mensaje = document.getElementById("mensaje-publica");
    if (mensaje) mensaje.style.display = "none";

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

        // ====== Botón Eliminar ======
    nuevaCard.querySelector(".eliminar-btn").addEventListener("click", () => {
      if (!confirm("¿Estás segura de que deseas eliminar esta publicación?")) return;
      const publicacionId = nuevaCard.dataset.publicacionId;

      fetch(`/publicaciones/${publicacionId}`, { method: "DELETE" })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            nuevaCard.remove();
            alert("✅ Publicación eliminada.");

            // 👇 Verifica si hay menos de 3 publicaciones y muestra el botón "+"
            const totalCards = document.querySelectorAll(".card-tarjeta").length;
            if (totalCards < 3) {
              const botonAdd = document.querySelector(".add-card");
              if (botonAdd) botonAdd.style.display = "";
            }

          } else {
            alert("❌ Error al eliminar: " + data.message);
          }
        })
        .catch(err => {
          console.error(err);
          alert("❌ Error: " + err.message);
        });
    });


        // ====== Botón Editar ======
    nuevaCard.querySelector(".bi-pencil-square").parentElement.addEventListener("click", () => {
    document.getElementById("editar-publicacion-id").value = datos.publicacion_id;
    document.getElementById("editar-titulo").value = datos.titulo;
    document.getElementById("editar-precio").value = datos.precio;
    document.getElementById("editar-descripcion").value = datos.descripcion;

    const categoriaSelectEditar = document.getElementById("editar-categoria");
    const subcategoriaSelectEditar = document.getElementById("editar-subcategoria");

   // Establece la categoría
categoriaSelectEditar.value = datos.categoria;

// Fuerza el evento change para que se activen listeners si existen
const eventoChange = new Event("change");
categoriaSelectEditar.dispatchEvent(eventoChange);

// Luego de un breve tiempo, llama a filtrarSubcategorias para asegurar selección
setTimeout(() => {
  // Asegurar que se use el subcategoriasData actualizado
  filtrarSubcategorias(datos.categoria, subcategoriaSelectEditar, datos.subcategoria);
}, 50); // Tiempo ligeramente mayor para asegurar que el DOM y los listeners ya están listos




    document.getElementById("formularioEditarModal").classList.remove("hidden");
  });



  }

  const editarFormulario = document.getElementById("formulario-editar-publicacion");

  editarFormulario.addEventListener("submit", function (e) {
    e.preventDefault();

    const publicacionId = document.getElementById("editar-publicacion-id").value;

    const datos = {
      titulo: document.getElementById("editar-titulo").value,
      categoria: document.getElementById("editar-categoria").value,
      subcategoria: document.getElementById("editar-subcategoria").value,
      precio: document.getElementById("editar-precio").value,
      descripcion: document.getElementById("editar-descripcion").value
    };

    fetch(`/publicaciones/${publicacionId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert("✅ Publicación actualizada correctamente.");
        document.getElementById("formularioEditarModal").classList.add("hidden");
        actualizarTarjetaPublicacion(data.data);
      } else {
        alert("❌ Error al actualizar: " + data.message);
      }
    })
    .catch(error => {
      console.error(error);
      alert("❌ Error: " + error.message);
    });
  });

  document.getElementById("cancelarEditar")?.addEventListener("click", () => {
    document.getElementById("formularioEditarModal").classList.add("hidden");
  });

  document.getElementById("cerrarEditarFormulario")?.addEventListener("click", () => {
    document.getElementById("formularioEditarModal").classList.add("hidden");
  });

    // Evento para cuando cambia la categoría en el formulario de editar
  document.getElementById("editar-categoria").addEventListener("change", function () {
    const categoriaId = this.value;
    const subcategoriaSelect = document.getElementById("editar-subcategoria");
    filtrarSubcategorias(categoriaId, subcategoriaSelect);
  });

  verificarLimitePublicaciones();

  function verificarLimitePublicaciones() {
  const totalPublicaciones = document.querySelectorAll(".card-tarjeta").length;
  const botonAdd = document.querySelector(".add-card");
  if (botonAdd) {
    botonAdd.style.display = totalPublicaciones >= 3 ? "none" : "flex";
  }
}

function actualizarTarjetaPublicacion(data) {
  const tarjeta = document.querySelector(`.card-tarjeta[data-publicacion-id="${data.publicacion_id}"]`);
  if (!tarjeta) return;

  tarjeta.querySelector(".profesion strong").textContent = data.titulo;
  tarjeta.querySelector(".descripcion-texto").textContent = data.descripcion;
  tarjeta.querySelector(".price").textContent = `COP ${data.precio}/h`;
}



});

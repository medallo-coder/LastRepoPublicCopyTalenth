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
});

document.addEventListener("DOMContentLoaded", () => {
    const modalLogin = document.getElementById("modalLoginContacto");
    const cerrarLogin = document.getElementById("cerrarLoginContacto");
    const isLoggedIn = document.body.getAttribute("data-logged-in") === "true";

    // Función para abrir modal login/contacto
    function manejarClickContacto(e) {
        e.preventDefault();
        e.stopPropagation();

        // Guardar si modal de ver más estaba abierto
        if (modalTarjeta && !modalTarjeta.classList.contains("hidden")) {
            modalTarjeta.dataset.prevOpen = "true";
            modalTarjeta.classList.add("hidden");
        }

        // Abrir modal login si no está logueado
        if (!isLoggedIn) {
            if (modalLogin) modalLogin.classList.remove("hidden");
        } else {
            console.log("Usuario logueado: abrir modal de contacto real si aplica.");
        }
    }

    // Asignar evento a todos los botones “Contactar experto”
    document.querySelectorAll(".contact-button").forEach(btn => {
        btn.addEventListener("click", manejarClickContacto);
    });

    // Cerrar modal login y reactivar modal “Ver más” si estaba abierto
    if (cerrarLogin) {
        cerrarLogin.addEventListener("click", () => {
            if (modalLogin) modalLogin.classList.add("hidden");

            // Reactivar modal de ver más si estaba abierto
            if (modalTarjeta && modalTarjeta.dataset.prevOpen === "true") {
                modalTarjeta.classList.remove("hidden");
                modalTarjeta.dataset.prevOpen = "false";
            }
        });
    }

    // Reaplicar evento para botón contactar dentro del modal "Ver más"
    document.addEventListener("click", function (e) {
        if (e.target && e.target.classList.contains("ver-mas")) {
            setTimeout(() => {
                const botonModalContacto = document.querySelector("#modalTarjeta .contact-button");
                if (botonModalContacto) {
                    botonModalContacto.addEventListener("click", manejarClickContacto, { once: true });
                }
            }, 200);
        }
    });

});

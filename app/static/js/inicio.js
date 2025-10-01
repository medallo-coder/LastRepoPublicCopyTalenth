document.addEventListener("DOMContentLoaded", function() {

    // --- Slider de Categorías ---
    const sliderCategorias = document.querySelector('.slider-categorias');
    const flechaCategoriasIzquierda = document.querySelector('.slider-categorias-contenedor .flecha.izquierda');
    const flechaCategoriasDerecha = document.querySelector('.slider-categorias-contenedor .flecha.derecha');

    // --- Sliders de Promos y Destacados ---
    const sliderPromos = document.querySelector(".contenedor .slider");
    const arrowPromosLeft = document.getElementById("arrowPromosLeft");
    const arrowPromosRight = document.getElementById("arrowPromosRight");

    const sliderDestacados = document.querySelector(".contenedor-destacados .slider");
    const arrowDestacadosLeft = document.getElementById("arrowDestacadosLeft");
    const arrowDestacadosRight = document.getElementById("arrowDestacadosRight");

    function getDynamicScrollAmount(sliderElement) {
        if (!sliderElement || !sliderElement.firstElementChild) return window.innerWidth <= 480 ? 365 : 600;
        const firstItem = sliderElement.firstElementChild;
        const itemWidth = firstItem.offsetWidth;
        const style = getComputedStyle(sliderElement);
        const gap = parseFloat(style.gap || '0');
        return itemWidth + gap;
    }

    function actualizarFlechas(sliderElement, prevArrow, nextArrow) {
        if (!sliderElement || !prevArrow || !nextArrow) return;
        if (sliderElement.scrollLeft <= 1) prevArrow.classList.add('inactiva'); else prevArrow.classList.remove('inactiva');
        if (sliderElement.scrollLeft + sliderElement.clientWidth >= sliderElement.scrollWidth - 1) nextArrow.classList.add('inactiva'); else nextArrow.classList.remove('inactiva');
    }

    // Configurar sliders con flechas
    if (sliderCategorias && flechaCategoriasIzquierda && flechaCategoriasDerecha) {
        flechaCategoriasIzquierda.addEventListener('click', () => sliderCategorias.scrollBy({ left: -getDynamicScrollAmount(sliderCategorias), behavior: 'smooth' }));
        flechaCategoriasDerecha.addEventListener('click', () => sliderCategorias.scrollBy({ left: getDynamicScrollAmount(sliderCategorias), behavior: 'smooth' }));
        actualizarFlechas(sliderCategorias, flechaCategoriasIzquierda, flechaCategoriasDerecha);
        sliderCategorias.addEventListener('scroll', () => actualizarFlechas(sliderCategorias, flechaCategoriasIzquierda, flechaCategoriasDerecha));
    }

    if (sliderPromos && arrowPromosLeft && arrowPromosRight) {
        arrowPromosLeft.addEventListener("click", () => sliderPromos.scrollBy({ left: -getDynamicScrollAmount(sliderPromos), behavior: "smooth" }));
        arrowPromosRight.addEventListener("click", () => sliderPromos.scrollBy({ left: getDynamicScrollAmount(sliderPromos), behavior: "smooth" }));
        actualizarFlechas(sliderPromos, arrowPromosLeft, arrowPromosRight);
        sliderPromos.addEventListener('scroll', () => actualizarFlechas(sliderPromos, arrowPromosLeft, arrowPromosRight));
    }

    if (sliderDestacados && arrowDestacadosLeft && arrowDestacadosRight) {
        arrowDestacadosLeft.addEventListener("click", () => sliderDestacados.scrollBy({ left: -getDynamicScrollAmount(sliderDestacados), behavior: "smooth" }));
        arrowDestacadosRight.addEventListener("click", () => sliderDestacados.scrollBy({ left: getDynamicScrollAmount(sliderDestacados), behavior: "smooth" }));
        actualizarFlechas(sliderDestacados, arrowDestacadosLeft, arrowDestacadosRight);
        sliderDestacados.addEventListener('scroll', () => actualizarFlechas(sliderDestacados, arrowDestacadosLeft, arrowDestacadosRight));
    }

    // --- Menú desplegable ---
    const menuButtons = document.querySelectorAll('.menu-button');
    const dropdownMenus = document.querySelectorAll('.menu-completo');
    window.cerrarMenu = function(elemento) {
        const menu = elemento.closest('.menu-completo');
        if (menu) menu.style.display = 'none';
    };
    menuButtons.forEach((button, index) => {
        const dropdownMenu = dropdownMenus[index];
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            const isVisible = dropdownMenu.style.display === 'block';
            dropdownMenus.forEach((menu) => (menu.style.display = 'none'));
            dropdownMenu.style.display = isVisible ? 'none' : 'block';
        });
    });
    document.addEventListener('click', () => dropdownMenus.forEach((menu) => (menu.style.display = 'none')));
    dropdownMenus.forEach((menu) => menu.addEventListener('click', (e) => e.stopPropagation()));

    // --- Descripción y Ver Más con modal ---
    // --- Descripción y Ver Más con modal ---
    const modalTarjeta = document.getElementById('modalTarjeta');
    const contenidoModal = document.getElementById('contenidoTarjeta');
    const cerrarTarjetaBtn = document.getElementById('cerrarTarjeta');

    const estaLogueado = document.body.getAttribute('data-logged-in') === 'true';
    const modalLogin = document.getElementById('modalLoginContacto');
    const closeLoginModal = document.getElementById('cerrarLoginContacto');

   // Función que devuelve el límite de caracteres según el tamaño de pantalla
   function getDescripcionLimit() {
    if (window.innerWidth <= 480) return 25;       // Celulares
    if (window.innerWidth <= 768) return 30;       // Tablets vertical
    if (window.innerWidth <= 1024) return 35;      // Tablets horizontal
    if (window.innerWidth <= 1366) return 40;   
    if (window.innerWidth <= 1600) return 50;     // Laptops grandes
    return 70;                                    // Pantallas muy grandes
  }

    // Función para aplicar recorte dinámico en todas las tarjetas
    function aplicarDescripcionResponsive() {
        const limite = getDescripcionLimit();

        document.querySelectorAll('.card-tarjeta').forEach(tarjeta => {
            const descripcionElem = tarjeta.querySelector('.descripcion');
            const verMasBtn = tarjeta.querySelector('.ver-mas');
            if (!descripcionElem || !verMasBtn) return;

            // Guardar descripción completa en data-completa si aún no existe
            if (!descripcionElem.dataset.completa) {
                descripcionElem.dataset.completa = descripcionElem.textContent.trim();
            }

            const textoOriginal = descripcionElem.dataset.completa;

            if (textoOriginal.length > limite) {
                descripcionElem.textContent = textoOriginal.substring(0, limite) + '...';
                verMasBtn.classList.remove('hidden');
            } else {
                descripcionElem.textContent = textoOriginal;
                verMasBtn.classList.add('hidden');
            }

            // Evento del botón "Ver más"
            verMasBtn.onclick = () => {
                const tarjetaClonada = tarjeta.cloneNode(true);

                // Poner la descripción completa
                tarjetaClonada.querySelector('.descripcion').textContent = textoOriginal;

                // Quitar "Ver más" en el modal
                const verMasClon = tarjetaClonada.querySelector('.ver-mas');
                if (verMasClon) verMasClon.remove();

                // Quitar menú en el modal
                const menuClon = tarjetaClonada.querySelector('.menu-button-container');
                if (menuClon) menuClon.remove();

                // Botón de contacto dentro del modal
                 const contactBtn = tarjetaClonada.querySelector('.contact-button');
                if (contactBtn) {
                    contactBtn.addEventListener('click', function(e) {
                        const estaLogueado = document.body.getAttribute('data-logged-in') === 'true';
                        if (!estaLogueado) {
                            e.preventDefault(); // 🚫 Evita la redirección
                            modalLogin.classList.remove('hidden');
                        } else {
                            console.log("Usuario logueado: abrir modal de contacto real si aplica.");
                        }
                    });
                }

                contenidoModal.innerHTML = '';
                contenidoModal.appendChild(tarjetaClonada);
                modalTarjeta.classList.remove('hidden');
            };
        });
    }

    // Aplicar al cargar la página
    aplicarDescripcionResponsive();

    // Reaplicar cuando cambia el tamaño de la ventana
    window.addEventListener('resize', aplicarDescripcionResponsive);

    // Cerrar modal de tarjeta
    cerrarTarjetaBtn.addEventListener('click', () => {
        modalTarjeta.classList.add('hidden');
        contenidoModal.innerHTML = '';
    });

    // --- Cerrar modal al hacer clic fuera ---
    window.addEventListener('click', function(e) {
        if (e.target === modalTarjeta) {
            modalTarjeta.classList.add('hidden');
            contenidoModal.innerHTML = '';
        }
        if (e.target === modalLogin) {
            modalLogin.classList.add('hidden');
        }
    });


    // --- Guardar publicaciones ---
    document.querySelectorAll('.guardar-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (btn.dataset.processing === "true") return;
            btn.dataset.processing = "true";

            const publicacionId = btn.dataset.id;
            const icono = btn.querySelector('i');
            const textoSpan = btn.querySelector('span');

            try {
                let url = `/guardar-publicacion/${publicacionId}`;
                let response = await fetch(url, { method: 'POST' });

                if (response.ok) {
                    let data = await response.json();
                    if (data.guardado) {
                        icono.classList.remove('bi-bookmark-check');
                        icono.classList.add('bi-bookmark-dash');
                        textoSpan.textContent = "Eliminar";
                    } else {
                        icono.classList.remove('bi-bookmark-dash');
                        icono.classList.add('bi-bookmark-check');
                        textoSpan.textContent = "Guardar";
                    }
                }
            } catch (error) {
                console.error("Error:", error);
            } finally {
                btn.dataset.processing = "false";
            }
        });
    });

    // --- Filtro de categorías ---
    const categorias = document.querySelectorAll("#sliderCategorias .categoria");
    const inputCategoria = document.getElementById("inputCategoria");
    const filtroForm = document.getElementById("filtroForm");
    categorias.forEach(categoria => {
        categoria.addEventListener("click", function () {
            const id = this.getAttribute("data-categoria-id");
            inputCategoria.value = id;
            filtroForm.submit();
        });
    });

    const cerrarLogin = document.getElementById("cerrarLoginContacto");

    // Manejo de abrir contacto
    function manejarClickContacto(e) {
        //e.preventDefault();
        //e.stopPropagation();

        // Guardar si modal "Ver más" estaba abierto
        if (modalTarjeta && !modalTarjeta.classList.contains("hidden")) {
            modalTarjeta.dataset.prevOpen = "true";
            modalTarjeta.classList.add("hidden"); // cerrar modal "Ver más"
        }

        // Abrir modal login si no está logueado
        if (!estaLogueado) {
            if (modalLogin) modalLogin.classList.remove("hidden");
        } else {
            console.log("Usuario logueado: abrir modal de contacto real si aplica.");
        }

    }

    // Contactar experto en tarjetas y modal "Ver más"
   document.querySelectorAll(".contact-button").forEach(btn => {
    btn.addEventListener("click", function(e) {
        const estaLogueado = document.body.getAttribute('data-logged-in') === 'true';
        
        if (!estaLogueado) {
            e.preventDefault(); // 🚫 Evita que se envíe el form
            const modalLogin = document.getElementById('modalLoginContacto');
            if (modalLogin) modalLogin.classList.remove('hidden');
        }
        // Si está logueado, el form se envía normalmente
    });
});


    // Cerrar modal login y reactivar modal "Ver más" si estaba abierto
    if (cerrarLogin) {
        cerrarLogin.addEventListener("click", () => {
            if (modalLogin) modalLogin.classList.add("hidden");

            if (modalTarjeta && modalTarjeta.dataset.prevOpen === "true") {
                modalTarjeta.classList.remove("hidden");
                modalTarjeta.dataset.prevOpen = "false";
            }
        });
    }

    // Contactar experto dentro de modal "Ver más" (al hacer click en Ver Más)
    document.addEventListener("click", function (e) {
        if (e.target && e.target.classList.contains("ver-mas")) {
            setTimeout(() => {
                const botonModalContacto = document.querySelector("#modalTarjeta .contact-button");
                if (botonModalContacto) {
                    // Aseguramos que solo se agregue una vez
                    botonModalContacto.addEventListener("click", manejarClickContacto, { once: true });
                }
            }, 200);
        }

    });

});

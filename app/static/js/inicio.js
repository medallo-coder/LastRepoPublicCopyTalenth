document.addEventListener("DOMContentLoaded", function() {

    // --- Selectores para todos los sliders y sus flechas ---
    // Slider de Categorías
    const sliderCategorias = document.querySelector('.slider-categorias');
    const flechaCategoriasIzquierda = document.querySelector('.slider-categorias-contenedor .flecha.izquierda');
    const flechaCategoriasDerecha = document.querySelector('.slider-categorias-contenedor .flecha.derecha');

    // Slider de "Servicios promocionados" (el que tenía id="slider")
    const sliderPromos = document.querySelector(".contenedor .slider"); // Asumiendo que .slider dentro de .contenedor es este
    const arrowPromosLeft = document.getElementById("arrowPromosLeft");
    const arrowPromosRight = document.getElementById("arrowPromosRight");

    // Slider de "Servicios destacados"
    const sliderDestacados = document.querySelector(".contenedor-destacados .slider");
    const arrowDestacadosLeft = document.getElementById("arrowDestacadosLeft");
    const arrowDestacadosRight = document.getElementById("arrowDestacadosRight");


    // --- Función para calcular el desplazamiento dinámicamente ---
    // Esta función es crucial para que el scroll sea preciso y no "quede de un lado"
    function getDynamicScrollAmount(sliderElement) {
        if (!sliderElement || !sliderElement.firstElementChild) {
            // Si el slider no tiene elementos, o no es un elemento HTML válido,
            // retorna un valor por defecto (se adapta al tamaño de pantalla como antes)
            return window.innerWidth <= 480 ? 365 : 600;
        }

        const firstItem = sliderElement.firstElementChild;
        const itemWidth = firstItem.offsetWidth; // Ancho del elemento incluyendo padding y borde

        // Obtener el valor de 'gap' del estilo computado del contenedor flex
        const style = getComputedStyle(sliderElement);
        const gap = parseFloat(style.gap || '0');

        // El desplazamiento es el ancho del primer elemento más el espacio (gap) entre elementos
        return itemWidth + gap;
    }


    // --- Función para actualizar el estado de las flechas (inactivas/activas) ---
    function actualizarFlechas(sliderElement, prevArrow, nextArrow) {
        if (!sliderElement || !prevArrow || !nextArrow) return; // Asegurarse de que los elementos existan

        // Desactivar flecha izquierda si está al inicio
        if (sliderElement.scrollLeft <= 1) { // Pequeño margen de error para 0
            prevArrow.classList.add('inactiva');
        } else {
            prevArrow.classList.remove('inactiva');
        }

        // Desactivar flecha derecha si está al final
        // Se usa un pequeño margen de error para problemas de redondeo de píxeles
        if (sliderElement.scrollLeft + sliderElement.clientWidth >= sliderElement.scrollWidth - 1) {
            nextArrow.classList.add('inactiva');
        } else {
            nextArrow.classList.remove('inactiva');
        }
    }


    // --- Configuración de Event Listeners para cada slider ---

    // Slider de Categorías
    if (sliderCategorias && flechaCategoriasIzquierda && flechaCategoriasDerecha) {
        // Evento de click para la flecha izquierda
        flechaCategoriasIzquierda.addEventListener('click', () => {
            const scrollAmount = getDynamicScrollAmount(sliderCategorias);
            sliderCategorias.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
            // No es necesario setTimeout aquí, el evento 'scroll' se encargará de actualizar las flechas
        });

        // Evento de click para la flecha derecha
        flechaCategoriasDerecha.addEventListener('click', () => {
            const scrollAmount = getDynamicScrollAmount(sliderCategorias);
            sliderCategorias.scrollBy({ left: scrollAmount, behavior: 'smooth' });
            // No es necesario setTimeout aquí
        });

        // Actualizar flechas al cargar la página
        actualizarFlechas(sliderCategorias, flechaCategoriasIzquierda, flechaCategoriasDerecha);
        // Actualizar flechas cuando el usuario hace scroll manualmente (con el mouse o arrastrando)
        sliderCategorias.addEventListener('scroll', () => {
            actualizarFlechas(sliderCategorias, flechaCategoriasIzquierda, flechaCategoriasDerecha);
        });
    }

    // Slider de "Servicios promocionados"
    if (sliderPromos && arrowPromosLeft && arrowPromosRight) {
        arrowPromosLeft.addEventListener("click", () => {
            const scrollAmount = getDynamicScrollAmount(sliderPromos);
            sliderPromos.scrollBy({ left: -scrollAmount, behavior: "smooth" });
        });

        arrowPromosRight.addEventListener("click", () => {
            const scrollAmount = getDynamicScrollAmount(sliderPromos);
            sliderPromos.scrollBy({ left: scrollAmount, behavior: "smooth" });
        });

        actualizarFlechas(sliderPromos, arrowPromosLeft, arrowPromosRight);
        sliderPromos.addEventListener('scroll', () => {
            actualizarFlechas(sliderPromos, arrowPromosLeft, arrowPromosRight);
        });
    }

    // Slider de "Servicios destacados"
    if (sliderDestacados && arrowDestacadosLeft && arrowDestacadosRight) {
        arrowDestacadosLeft.addEventListener("click", () => {
            const scrollAmount = getDynamicScrollAmount(sliderDestacados);
            sliderDestacados.scrollBy({ left: -scrollAmount, behavior: "smooth" });
        });

        arrowDestacadosRight.addEventListener("click", () => {
            const scrollAmount = getDynamicScrollAmount(sliderDestacados);
            sliderDestacados.scrollBy({ left: scrollAmount, behavior: "smooth" });
        });

        actualizarFlechas(sliderDestacados, arrowDestacadosLeft, arrowDestacadosRight);
        sliderDestacados.addEventListener('scroll', () => {
            actualizarFlechas(sliderDestacados, arrowDestacadosLeft, arrowDestacadosRight);
        });
    }


    // --- Lógica para el menú desplegable (existente, se mantiene) ---
    const menuButtons = document.querySelectorAll('.menu-button');
    const dropdownMenus = document.querySelectorAll('.menu-completo');

    menuButtons.forEach((button, index) => {
        const dropdownMenu = dropdownMenus[index];

        button.addEventListener('click', (e) => {
            e.stopPropagation();
            const isVisible = dropdownMenu.style.display === 'block';

            dropdownMenus.forEach((menu) => (menu.style.display = 'none'));
            dropdownMenu.style.display = isVisible ? 'none' : 'block';
        });
    });

    document.addEventListener('click', () => {
        dropdownMenus.forEach((menu) => (menu.style.display = 'none'));
    });

    dropdownMenus.forEach((menu) => {
        menu.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    });


    // --- Lógica para las tarjetas (descripción y "Ver Más", existente, se mantiene) ---
    const tarjetas = document.querySelectorAll('.card-tarjeta');

    tarjetas.forEach(tarjeta => {
        const descripcionElem = tarjeta.querySelector('.descripcion');
        const verMasBtn = tarjeta.querySelector('.ver-mas');

        // Asegurarse de que descripcionElem y verMasBtn existan antes de continuar
        if (!descripcionElem || !verMasBtn) return;

        const textoOriginal = descripcionElem.textContent.trim();

        if (textoOriginal.length > 70) {
            descripcionElem.textContent = textoOriginal.substring(0, 70) + '...';
            verMasBtn.classList.remove('hidden');

            verMasBtn.addEventListener('click', () => {
                const tarjetaClonada = tarjeta.cloneNode(true);
                tarjetaClonada.querySelector('.descripcion').textContent = textoOriginal;

                const verMasClon = tarjetaClonada.querySelector('.ver-mas');
                if (verMasClon) verMasClon.remove(); // Eliminar el botón "Ver Más" del clon

                const menuClon = tarjetaClonada.querySelector('.menu-button-container');
                if (menuClon) menuClon.remove(); // Eliminar el botón de menú del clon

                const contenedorModal = document.getElementById('contenidoTarjeta');
                if (contenedorModal) { // Asegurarse de que el contenedor exista
                    contenedorModal.innerHTML = '';
                    contenedorModal.appendChild(tarjetaClonada);
                }

                const modalTarjeta = document.getElementById('modalTarjeta');
                if (modalTarjeta) { // Asegurarse de que el modal exista
                    modalTarjeta.classList.remove('hidden');
                }
            });
        } else {
            verMasBtn.classList.add('hidden');
        }
    });

    const cerrarTarjetaBtn = document.getElementById('cerrarTarjeta');
    if (cerrarTarjetaBtn) { // Asegurarse de que el botón de cerrar exista
        cerrarTarjetaBtn.addEventListener('click', () => {
            const modalTarjeta = document.getElementById('modalTarjeta');
            if (modalTarjeta) {
                modalTarjeta.classList.add('hidden');
            }
        });
    }

     const btnAbrir = document.getElementById('abrirModalReporte');
    const modal = document.getElementById('modalReporte');
    const btnCerrar = document.getElementById('cerrarModalReporte');
    const btnCancelar = document.getElementById('cancelarModalReporte');

    btnAbrir.addEventListener('click', (e) => {
        e.preventDefault();
        modal.style.display = 'flex';
    });

    btnCerrar.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    btnCancelar.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
        modal.style.display = 'none';
        }
    });            
});

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

    // --- Descripción y Ver Más ---
    document.querySelectorAll('.card-tarjeta').forEach(tarjeta => {
        const descripcionElem = tarjeta.querySelector('.descripcion');
        const verMasBtn = tarjeta.querySelector('.ver-mas');
        if (!descripcionElem || !verMasBtn) return;
        const textoOriginal = descripcionElem.textContent.trim();
        if (textoOriginal.length > 70) {
            descripcionElem.textContent = textoOriginal.substring(0, 70) + '...';
            verMasBtn.classList.remove('hidden');
            verMasBtn.addEventListener('click', () => {
                const tarjetaClonada = tarjeta.cloneNode(true);
                tarjetaClonada.querySelector('.descripcion').textContent = textoOriginal;
                const verMasClon = tarjetaClonada.querySelector('.ver-mas'); if (verMasClon) verMasClon.remove();
                const menuClon = tarjetaClonada.querySelector('.menu-button-container'); if (menuClon) menuClon.remove();
                const contenedorModal = document.getElementById('contenidoTarjeta');
                if (contenedorModal) { contenedorModal.innerHTML = ''; contenedorModal.appendChild(tarjetaClonada); }
                const modalTarjeta = document.getElementById('modalTarjeta'); if (modalTarjeta) modalTarjeta.classList.remove('hidden');
            });
        } else { verMasBtn.classList.add('hidden'); }
    });

    const cerrarTarjetaBtn = document.getElementById('cerrarTarjeta');
    if (cerrarTarjetaBtn) cerrarTarjetaBtn.addEventListener('click', () => {
        const modalTarjeta = document.getElementById('modalTarjeta');
        if (modalTarjeta) modalTarjeta.classList.add('hidden');
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
            console.log("Respuesta servidor:", data);

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


    const contactButtons = document.querySelectorAll('.contact-button');
    const modalLogin = document.getElementById('modalLoginContacto');
    const closeLoginModal = document.getElementById('cerrarLoginContacto');

    // Este valor lo pasamos desde Flask al JS
    const estaLogueado = document.body.getAttribute('data-logueado') === 'true';

    contactButtons.forEach(button => {
      button.addEventListener('click', function () {
        if (!estaLogueado) {
          modalLogin.classList.remove('hidden');
        } else {
          // Aquí puedes redirigir al chat o página de contacto real
          console.log("Usuario logueado, se puede contactar al experto.");
        }
      });
    });

    // Botón para cerrar el modal
    closeLoginModal.addEventListener('click', function () {
      modalLogin.classList.add('hidden');
    });

    // También cerrarlo si se hace clic fuera del modal
    window.addEventListener('click', function (e) {
      if (e.target === modalLogin) {
        modalLogin.classList.add('hidden');
      }
    });
  

    
});

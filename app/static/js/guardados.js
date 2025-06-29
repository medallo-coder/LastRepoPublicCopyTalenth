
const slider = document.getElementById("slider");
const buttons = document.querySelectorAll(".arrow-btn");

buttons[0].addEventListener("click", () => {
  slider.scrollLeft -= 300;
});
buttons[1].addEventListener("click", () => {
  slider.scrollLeft += 300;
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
// Abrir modal
function openModal() {
  document.getElementById('modal').style.display = 'block';
  document.getElementById('overlay').style.display = 'block';
}

// Cerrar modal
function closeModal() {
  document.getElementById('modal').style.display = 'none';
  document.getElementById('overlay').style.display = 'none';
}

// Alternar menú desplegable
function toggleMenu(event) {
  event.stopPropagation();
  const menu = event.target.nextElementSibling;
  menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}

// Manejar opciones del menú
function handleOption(option) {
  alert(`Seleccionaste: ${option}`);
}



// nav y menu amburguesa

// Selecciona todos los botones de opciones
document.querySelectorAll('.options-button').forEach(button => {
  button.addEventListener('click', (event) => {
      // Encuentra el menú desplegable relacionado
      const menu = button.parentElement.querySelector('.options-menu');

      // Alterna la visibilidad del menú
      menu.style.display = menu.style.display === 'block' ? 'none' : 'block';

      // Cierra otros menús abiertos
      document.querySelectorAll('.options-menu').forEach(otherMenu => {
          if (otherMenu !== menu) {
              otherMenu.style.display = 'none';
          }
      });

      // Detiene la propagación del evento para que el clic fuera cierre el menú
      event.stopPropagation();
  });
});

// Cierra el menú si se hace clic fuera de él
document.addEventListener('click', () => {
  document.querySelectorAll('.options-menu').forEach(menu => {
      menu.style.display = 'none';
  });
});



const navbar = document.querySelector('.navbar');

let isDragging = false;
let startX;
let scrollLeft;

navbar.addEventListener('mousedown', (e) => {
  isDragging = true;
  navbar.classList.add('dragging');
  startX = e.pageX - navbar.offsetLeft;
  scrollLeft = navbar.scrollLeft;
});

navbar.addEventListener('mouseleave', () => {
  isDragging = false;
  navbar.classList.remove('dragging');
});

navbar.addEventListener('mouseup', () => {
  isDragging = false;
  navbar.classList.remove('dragging');
});

navbar.addEventListener('mousemove', (e) => {
  if (!isDragging) return;
  e.preventDefault();
  const x = e.pageX - navbar.offsetLeft;
  const walk = (x - startX) * 2; // Ajusta la velocidad del desplazamiento
  navbar.scrollLeft = scrollLeft - walk;
});

// Soporte para dispositivos táctiles
navbar.addEventListener('touchstart', (e) => {
  startX = e.touches[0].pageX - navbar.offsetLeft;
  scrollLeft = navbar.scrollLeft;
});

navbar.addEventListener('touchmove', (e) => {
  const x = e.touches[0].pageX - navbar.offsetLeft;
  const walk = (x - startX) * 2;
  navbar.scrollLeft = scrollLeft - walk;
});



document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll('.navbar a');
  links.forEach(link => {
    // Verifica si el href del enlace coincide con la parte final de la URL actual
    if (link.href.endsWith("my_public.html") || link.href.endsWith("historial_c.html")) {
      if (link.href === window.location.href) {
        link.classList.add('active');
      }
    }
  });
});


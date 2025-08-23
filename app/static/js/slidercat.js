document.addEventListener("DOMContentLoaded", () => {
    const slider = document.getElementById("sliderCategorias");

    // ========== DESPLAZAMIENTO CON MOUSE ==========
    let isMouseDown = false;
    let mouseStartX = 0;
    let mouseScrollStart = 0;

    slider.addEventListener("mousedown", (e) => {
        isMouseDown = true;
        mouseStartX = e.pageX;
        mouseScrollStart = slider.scrollLeft;
        slider.classList.add("grabbing"); // opcional: para cambiar el cursor
    });

    slider.addEventListener("mousemove", (e) => {
        if (!isMouseDown) return;
        e.preventDefault();
        const deltaX = e.pageX - mouseStartX;
        slider.scrollLeft = mouseScrollStart - deltaX;
    });

    document.addEventListener("mouseup", () => {
        isMouseDown = false;
        slider.classList.remove("grabbing");
    });

    slider.addEventListener("mouseleave", () => {
        isMouseDown = false;
        slider.classList.remove("grabbing");
    });

    // ========== DESPLAZAMIENTO TÁCTIL NATURAL ==========
    let touchStartX = 0;
    let touchScrollStart = 0;

    slider.addEventListener("touchstart", (e) => {
        touchStartX = e.touches[0].pageX;
        touchScrollStart = slider.scrollLeft;
    });

    slider.addEventListener("touchmove", (e) => {
        const currentX = e.touches[0].pageX;
        const deltaX = currentX - touchStartX;
        slider.scrollLeft = touchScrollStart - deltaX;
    });
});



//flechas
document.addEventListener("DOMContentLoaded", () => {
const slider = document.getElementById("sliderCategorias");
const flechaIzq = document.getElementById("flechaIzq");
const flechaDer = document.getElementById("flechaDer");

flechaIzq.addEventListener("click", () => {
  slider.scrollLeft -= 200; // Mueve a la izquierda
});

flechaDer.addEventListener("click", () => {
  slider.scrollLeft += 200; // Mueve a la derecha
});
});
//opacidad flechas
document.addEventListener("DOMContentLoaded", () => {
const slider = document.getElementById("sliderCategorias");
const flechaIzq = document.getElementById("flechaIzq");
const flechaDer = document.getElementById("flechaDer");

// Función para actualizar la visibilidad de las flechas
function actualizarFlechas() {
  if (slider.scrollLeft === 0) {
      flechaIzq.classList.add("desactivada"); // Opaca si está al inicio
  } else {
      flechaIzq.classList.remove("desactivada");
  }

  if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth) {
      flechaDer.classList.add("desactivada"); // Opaca si está al final
  } else {
      flechaDer.classList.remove("desactivada");
  }
}

// Detectar cambios en el scroll
slider.addEventListener("scroll", actualizarFlechas);

// Acciones al hacer clic en las flechas
flechaIzq.addEventListener("click", () => {
  slider.scrollLeft -= 200;
  actualizarFlechas();
});

flechaDer.addEventListener("click", () => {
  slider.scrollLeft += 200;
  actualizarFlechas();
});

// Llamamos a la función una vez al cargar la página
actualizarFlechas();
});
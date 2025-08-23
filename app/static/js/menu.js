
document.addEventListener("DOMContentLoaded", function () {
    const menu = document.querySelector('.menu');
    const menuid = document.getElementById('menuid');
    const sidebar = document.getElementById('sidebar');

    // Abrir / cerrar el menú
    menuid.addEventListener('click', (event) => {
        event.stopPropagation(); // Evita que el clic afecte otros elementos
        menu.classList.toggle("active"); // Alterna la clase active en el menú (para la "X")
        sidebar.classList.toggle("click"); // Abre o cierra el sidebar
    });

    // Cierra el menú si se hace clic fuera de él
    document.addEventListener("click", function (event) {
        // Si el clic fue fuera del sidebar y el menú
        if (!sidebar.contains(event.target) && !menu.contains(event.target)) {
            sidebar.classList.remove("click"); // Cierra el sidebar
            menu.classList.remove("active"); // Revertir el menú a la hamburguesa
        }
    });

    // Evitar que el clic en el sidebar cierre el menú (el clic dentro del sidebar no debe cerrar el menú)
    sidebar.addEventListener('click', (event) => {
        event.stopPropagation(); // Detener la propagación para que el clic no cierre el menú
    });
});




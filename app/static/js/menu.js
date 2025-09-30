document.addEventListener("DOMContentLoaded", function () {
    const menu = document.querySelector('.menu');
    const menuid = document.getElementById('menuid');
    const sidebar = document.getElementById('sidebar');
    const nav = document.querySelector(".header_nav"); 
    const closeBtn = document.getElementById('closeSidebar'); // 👈 la X
    let lastScrollTop = 0; 

    // Abrir / cerrar el menú (hamburguesa)
    menuid.addEventListener('click', (event) => {
        event.stopPropagation(); 
        menu.classList.toggle("active"); 
        sidebar.classList.toggle("click"); 
    });

    // Cerrar el menú con la X
    closeBtn.addEventListener('click', () => {
        sidebar.classList.remove("click"); // Cierra el sidebar
        menu.classList.remove("active");   // Revertir la hamburguesa
    });

    // Cierra el menú si se hace clic fuera de él
    document.addEventListener("click", function (event) {
        if (!sidebar.contains(event.target) && !menu.contains(event.target)) {
            sidebar.classList.remove("click"); 
            menu.classList.remove("active"); 
        }
    });

    // Evitar que el clic en el sidebar lo cierre
    sidebar.addEventListener('click', (event) => {
        event.stopPropagation(); 
    });

    // ---- NAV OCULTARSE AL SCROLL ----
    window.addEventListener("scroll", () => {
        const scrollTop = window.scrollY || document.documentElement.scrollTop;

        if (scrollTop > lastScrollTop) {
            nav.classList.add("hide");
        } else {
            nav.classList.remove("hide");
        }

        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });
});

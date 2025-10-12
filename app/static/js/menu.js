document.addEventListener("DOMContentLoaded", function () {
    const menu = document.querySelector('.menu');
    const menuid = document.getElementById('menuid');
    const sidebar = document.getElementById('sidebar');
    const nav = document.querySelector(".header_nav"); 
    const closeBtn = document.getElementById('closeSidebar'); // 👈 la X
    let lastScrollTop = 0; 

    // Abrir / cerrar el menú (hamburguesa)
    // Abrir / cerrar el menú (hamburguesa)
menuid.addEventListener('click', (event) => {
    event.stopPropagation(); 
    menu.classList.toggle("active"); 
    sidebar.classList.toggle("click"); 

    // Bloquear scroll cuando el menú está abierto
    if (sidebar.classList.contains("click")) {
        document.body.classList.add("no-scroll");
    } else {
        document.body.classList.remove("no-scroll");
    }
});

// Cerrar el menú con la X
closeBtn.addEventListener('click', () => {
    sidebar.classList.remove("click"); 
    menu.classList.remove("active");   
    document.body.classList.remove("no-scroll"); // quitar bloqueo scroll
});

// Cierra el menú si se hace clic fuera de él
document.addEventListener("click", function (event) {
    if (!sidebar.contains(event.target) && !menu.contains(event.target)) {
        sidebar.classList.remove("click"); 
        menu.classList.remove("active"); 
        document.body.classList.remove("no-scroll"); // quitar bloqueo scroll
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

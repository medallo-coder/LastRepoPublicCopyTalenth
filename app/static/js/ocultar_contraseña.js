document.addEventListener("DOMContentLoaded", () => {
    const toggles = document.querySelectorAll(".toggle-pass");

    toggles.forEach((icon) => {
        // Si tiene el atributo data-target, usa ese ID
        const targetId = icon.getAttribute("data-target");

        // Si no tiene data-target, intenta encontrar el input anterior (para login/registro antiguos)
        const input = targetId
            ? document.getElementById(targetId)
            : icon.previousElementSibling;

        if (!input) return;

        icon.addEventListener("click", () => {
            const isPassword = input.type === "password";
            input.type = isPassword ? "text" : "password";
            icon.classList.toggle("bi-eye-fill", !isPassword);
            icon.classList.toggle("bi-eye-slash-fill", isPassword);
        });
    });
});

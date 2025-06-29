//ojo de ocultar o ver contraseña
const toggles = document.querySelectorAll(".toggle-pass");

    toggles.forEach((icon, index) => {
        const input = document.getElementById(`pass${index + 1}`);

        icon.addEventListener("click", () => {
            if (input.type === "password") {
                input.type = "text";
                icon.classList.remove('bi-eye-fill');
                icon.classList.add('bi-eye-slash-fill');
            } else {
                input.type = "password";
                icon.classList.add('bi-eye-fill');
                icon.classList.remove('bi-eye-slash-fill');
            }
        });
    });
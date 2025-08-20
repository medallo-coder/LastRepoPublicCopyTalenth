
const botonesAbrir = document.querySelectorAll(".abrir-modal-reporte");
  const modal = document.getElementById("modalReporte");
  const btnCancelar = document.getElementById("cancelarModalReporte");

  // Abrir modal
  botonesAbrir.forEach((boton) => {
    boton.addEventListener("click", (e) => {
      e.preventDefault();
      modal.style.display = "flex";
    });
  });

  // Cerrar con botón cancelar
  btnCancelar.addEventListener("click", () => {
    modal.style.display = "none";
  });

  // Cerrar haciendo clic fuera del contenido
  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
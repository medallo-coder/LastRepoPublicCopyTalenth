document.addEventListener("DOMContentLoaded", () => {
  const botonesAbrir = document.querySelectorAll(".abrir-modal-reporte");
  const modal = document.getElementById("modalReporte");
  const btnCancelar = document.getElementById("cancelarModalReporte");

  if (!modal) {
    console.error("[Modal Reporte] El modal no se encontró en el DOM.");
    return;
  }

  // Abrir modal
  botonesAbrir.forEach((boton) => {
    boton.addEventListener("click", (e) => {
      e.preventDefault();

      // Tomar valores de los atributos data- del botón
      const reportadoId = boton.getAttribute("data-usuario-reportado");
      const reportadorId = boton.getAttribute("data-usuario");

      // Insertarlos en los inputs ocultos del modal
      const inputReportado = document.getElementById("reportado-id-input");
      const inputReportador = document.getElementById("reportador-id-input");

      if (inputReportado) inputReportado.value = reportadoId;
      if (inputReportador) inputReportador.value = reportadorId;

      modal.style.display = "flex";
    });
  });

  // Cerrar con botón cancelar
  if (btnCancelar) {
    btnCancelar.addEventListener("click", () => {
      modal.style.display = "none";
    });
  }

  // Cerrar haciendo clic fuera del contenido
  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});

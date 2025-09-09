document.addEventListener("DOMContentLoaded", () => {
  console.log("[modal_reportar.js] cargado ✅");

  const botonesAbrir = document.querySelectorAll(".abrir-modal-reporte");
  const modal = document.getElementById("modalReporte");
  const btnCancelar = document.getElementById("cancelarModalReporte");

  if (!modal) {
    console.error("[Modal Reporte] No se encontró el modal en el DOM.");
    return;
  }

  botonesAbrir.forEach((boton) => {
    boton.addEventListener("click", (e) => {
      e.preventDefault();

      console.log("[Modal Reporte] botón clickeado");

      // Tomar valores de los atributos data- del botón
      const reportadoId = boton.getAttribute("data-usuario-reportado");

      // Inputs ocultos en el modal
      const inputReportado = document.getElementById("reportado-id-input");
      const inputReportador = document.getElementById("reportador-id-input");

      // Asignar valores
      if (inputReportado) inputReportado.value = reportadoId;

      // Ojo 👇 este NO se toca porque ya viene con {{ id_usuario_logueado }}
      // if (inputReportador) inputReportador.value = algo

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

// modal_reportar.js
document.addEventListener("DOMContentLoaded", () => {
  console.log("[modal_reportar.js] cargado ✅");

  const modal = document.getElementById("modalReporte") || document.getElementById("modalReportar");
  const btnCancelar = document.getElementById("cancelarModalReporte");

  if (!modal) {
    console.error("[Modal Reporte] No se encontró el modal en el DOM.");
    return;
  }

  document.querySelectorAll(".abrir-modal-reporte").forEach((boton) => {
    boton.addEventListener("click", (e) => abrirModal(e, boton, modal));
  });

  document.addEventListener("click", (e) => {
    const boton = e.target.closest(".abrir-modal-reporte");
    if (boton) abrirModal(e, boton, modal);
    if (e.target === modal) modal.style.display = "none";
  });

  if (btnCancelar) {
    btnCancelar.addEventListener("click", () => {
      modal.style.display = "none";
    });
  }

  function abrirModal(e, boton, modal) {
    e.preventDefault();
    console.log("[Modal Reporte] botón clickeado");

    // --- Reportado (ya te funcionaba) ---
    const reportadoId = boton.getAttribute("data-usuario-reportado");
    const inputReportado = document.getElementById("reportado-id-input");
    if (inputReportado) inputReportado.value = reportadoId || "";

    // --- Reportador (lo que faltaba) ---
    const inputReportador = document.getElementById("reportador-id-input");
    if (inputReportador && !inputReportador.value) {
      const currentUserInput = document.getElementById("currentUserId");
      const reportadorId =
        (currentUserInput && currentUserInput.value) ||
        boton.getAttribute("data-usuario") ||
        boton.getAttribute("data-reportador-id") ||
        ""; // último recurso

      inputReportador.value = reportadorId;
    }

    // Ocultar menús contextuales
    document.querySelectorAll(".contact-menu").forEach((m) => m.classList.add("oculto"));

    modal.style.display = "flex";
  }
});

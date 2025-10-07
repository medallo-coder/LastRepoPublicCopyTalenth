document.addEventListener("DOMContentLoaded", () => {
  console.log("[modal_reportar.js] cargado ✅");

  const modal = document.getElementById("modalReporte") || document.getElementById("modalReportar");
  const btnCancelar = document.getElementById("cancelarModalReporte");

  if (!modal) {
    console.error("[Modal Reporte] No se encontró el modal en el DOM.");
    return;
  }

  // 🔹 1. Escucha botones existentes (inicio)
  document.querySelectorAll(".abrir-modal-reporte").forEach((boton) => {
    boton.addEventListener("click", (e) => abrirModal(e, boton, modal));
  });

  // 🔹 2. Delegación para botones agregados después (mensajería)
  document.addEventListener("click", (e) => {
    const boton = e.target.closest(".abrir-modal-reporte");
    if (boton) abrirModal(e, boton, modal);

    if (e.target === modal) modal.style.display = "none";
  });

  // 🔹 3. Cerrar con botón cancelar
  if (btnCancelar) {
    btnCancelar.addEventListener("click", () => {
      modal.style.display = "none";
    });
  }

  // 🔹 Función reutilizable para abrir el modal
  function abrirModal(e, boton, modal) {
  e.preventDefault();
  console.log("[Modal Reporte] botón clickeado");

  const reportadoId = boton.getAttribute("data-usuario-reportado");
  const inputReportado = document.getElementById("reportado-id-input");

  if (inputReportado) inputReportado.value = reportadoId;

  // 🔸 ➕ Agrega esta línea:
  document.querySelectorAll('.contact-menu').forEach(m => m.classList.add('oculto'));

  modal.style.display = "flex";
}

});

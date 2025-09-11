// Abrir modal
function abrirModalPromocionar() {
  const modal = document.getElementById("modalPromocionarPublicacion");
  if(modal) modal.style.display = "flex";
}

// Cerrar modal
function cerrarModalPromocionar() {
  const modal = document.getElementById("modalPromocionarPublicacion");
  if(modal) modal.style.display = "none";
}

// Cierre haciendo clic fuera del contenido
document.addEventListener("DOMContentLoaded", function() {
  const modal = document.getElementById("modalPromocionarPublicacion");
  if(modal) {
    modal.addEventListener("click", function(e) {
      if(e.target === modal) {
        cerrarModalPromocionar();
      }
    });
  }
});

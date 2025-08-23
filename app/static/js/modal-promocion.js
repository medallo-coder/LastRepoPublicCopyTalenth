// Mostrar el modal
function mostrarModal() {
  const modal = document.getElementById("modalPromocion");
  if (modal) {
    modal.style.display = "flex";
  }
}

// Cerrar el modal
function cerrarModal() {
  const modal = document.getElementById("modalPromocion");
  if (modal) {
    modal.style.display = "none";
  }
}

// Acción al hacer clic en "Obtener promoción"
function obtenerPromocion() {
  // Aquí puedes redirigir o iniciar proceso de compra
  console.log("Usuario desea promocionar");
  cerrarModal();
}

// Cierre haciendo clic en la sombra (overlay)
document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("modalPromocion");
  if (modal) {
    modal.addEventListener("click", function (e) {
      if (e.target === modal) {
        cerrarModal();
      }
    });
  }
});




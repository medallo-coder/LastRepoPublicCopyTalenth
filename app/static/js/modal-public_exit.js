function abrirModalPromocionar() {
  document.getElementById("modalPromocionarPublicacion").style.display = "block";
}

function cerrarModalPromocionar() {
  document.getElementById("modalPromocionarPublicacion").style.display = "none";
}

function redirigirAPromocion() {
  window.location.href = "/promocionar-publicacion";  // Cambia si tienes otra ruta real
}

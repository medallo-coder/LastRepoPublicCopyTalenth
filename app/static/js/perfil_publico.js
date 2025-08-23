
// js de fot para ver de mas grande
document.addEventListener('DOMContentLoaded', () => {
  const imagenes = document.querySelectorAll('.image');
  const modal = document.getElementById('imagenModal');
  const modalImg = document.getElementById('imagenAmpliada');
  const cerrar = document.getElementById('cerrarModal');

  imagenes.forEach(img => {
    img.addEventListener('click', () => {
      modal.style.display = 'flex';
      modalImg.src = img.src;
    });
  });

  cerrar.addEventListener('click', () => {
    modal.style.display = 'none';
  });
});

// Desaparecer los mensajes que ya existían (de los flash normales)
setTimeout(function() {
  const messages = document.querySelectorAll('.alert');
  messages.forEach(message => {
    message.style.opacity = '0';
    setTimeout(() => message.remove(), 500);
  });
}, 3000);

// Mostrar mensaje flotante dinámico
function mostrarMensajeFlotante(mensaje, categoria) {
  const contenedor = document.querySelector('.messages-container');
  if (!contenedor) return;

  const alerta = document.createElement('div');
  alerta.className = `alert ${categoria}`;
  alerta.textContent = mensaje;
  contenedor.appendChild(alerta);

  setTimeout(() => {
    alerta.style.opacity = '0';
    setTimeout(() => alerta.remove(), 500);
  }, 3000);
}

// Lógica de guardar
document.querySelectorAll('.guardar-btn').forEach(btn => {
  btn.addEventListener('click', function(event) {
    event.preventDefault();  // 💥 Para evitar que el <a> haga reload
    const id = this.dataset.id;
    fetch(`/guardar-publicacion/${id}`, {
      method: 'POST'
    })
    .then(async res => {
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.message || `Error ${res.status}`);
      }
      mostrarMensajeFlotante(data.message, 'success');
    })
    .catch(err => {
      mostrarMensajeFlotante(err.message, 'error');
    });
  });
});

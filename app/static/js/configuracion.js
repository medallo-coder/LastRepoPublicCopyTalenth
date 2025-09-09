// Mostrar formulario cambiar contraseña
document.getElementById('cambiarContraseñaBtn').addEventListener('click', () => {
  const formulario = document.getElementById('formularioCambio');
  formulario.classList.remove('hidden');
  formulario.scrollIntoView({ behavior: 'smooth' });
  document.getElementById('cambiarContraseñaBtn').style.display = 'none';
});

// Ocultar formulario cambiar contraseña
document.getElementById('cancelarBtn').addEventListener('click', () => {
  const formulario = document.getElementById('formularioCambio');
  formulario.classList.add('hidden');
  document.getElementById('passwordForm').reset();
  document.getElementById('cambiarContraseñaBtn').style.display = 'inline-block';
});

// Mostrar formulario eliminar cuenta
document.getElementById('eliminarCuentaBtn').addEventListener('click', () => {
  const formulario = document.getElementById('formularioEliminar');
  formulario.classList.remove('hidden');
  formulario.scrollIntoView({ behavior: 'smooth' });
  document.getElementById('eliminarCuentaBtn').style.display = 'none';
});

// Ocultar formulario eliminar cuenta
document.getElementById('cancelarEliminarBtn').addEventListener('click', () => {
  const formulario = document.getElementById('formularioEliminar');
  formulario.classList.add('hidden');
  document.getElementById('eliminarForm').reset();
  document.getElementById('eliminarCuentaBtn').style.display = 'inline-block';
});

// Formatear fecha registro al cargar el DOM
document.addEventListener('DOMContentLoaded', function() {
  const fechaRegistroText = document.getElementById('fecha_registro').textContent;
  
  // Suponemos que la fecha viene en formato "2025-05-01" o similar
  const fecha = new Date(fechaRegistroText);

  // Diccionario de meses en español
  const mesesEspanol = [
      'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ];

  // Obtenemos el mes (0 basado) y el año
  const mes = fecha.getMonth();
  const anio = fecha.getFullYear();

  // Formateamos la fecha en el formato deseado
  const fechaFormateada = `Se unió en ${mesesEspanol[mes]} de ${anio}`;

  // Actualizamos el contenido del <p> con la fecha formateada
  document.getElementById('fecha_registro').textContent = fechaFormateada;
});

// Referencias
const eliminarForm = document.getElementById('eliminarForm');
const btnMostrarModalEliminar = document.getElementById('btnEliminarCuentaForm');
const modalEliminarCuenta = document.getElementById('modalEliminarCuenta');
const btnCancelarEliminarModal = document.getElementById('cancelarEliminarModalBtn');
const btnConfirmarEliminar = document.getElementById('confirmarEliminarBtn');


// Cancelar en modal (ocultar modal)
btnCancelarEliminarModal.addEventListener('click', () => {
  modalEliminarCuenta.classList.add('hidden');
});

// Confirmar eliminar (enviar formulario)
btnConfirmarEliminar.addEventListener('click', () => {
  // Opcional: puedes bloquear el botón o mostrar loading
  eliminarForm.submit();
});

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('eliminarForm');
  const passInput = document.getElementById('pass4');
  const errorMsg = document.getElementById('mensajeErrorEliminar');
  const modal = document.getElementById('modalEliminarCuenta');
  const btnShow = document.getElementById('btnEliminarCuentaForm');
  const btnConfirm = document.getElementById('confirmarEliminarBtn');
  const btnCancel = document.getElementById('cancelarEliminarModalBtn');

  btnShow.addEventListener('click', async () => {
    const pass = passInput.value.trim();
    errorMsg.textContent = ''; // Limpiar errores anteriores

    if (!pass) {
      errorMsg.textContent = 'Por favor ingresa tu contraseña.';
      return;
    }

    try {
      const res = await fetch('/configuracion/validar_contrasena', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ contrasena: pass })
      });
      const json = await res.json();
      if (json.success) {
        modal.classList.remove('hidden');
      } else {
        errorMsg.textContent = json.message || 'Contraseña incorrecta.';
      }
    } catch {
      errorMsg.textContent = 'Error al validar la contraseña.';
    }
  });

  btnConfirm.addEventListener('click', () => form.submit());
  btnCancel.addEventListener('click', () => modal.classList.add('hidden'));
  
});

// Cerrar modal si se hace clic fuera del contenido del modal
modalEliminarCuenta.addEventListener('click', (event) => {
  if (event.target === modalEliminarCuenta) {
    modalEliminarCuenta.classList.add('hidden');
  }
});


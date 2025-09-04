const form = document.querySelector("form");
const pass1 = document.getElementById("pass1");
const pass2 = document.getElementById("pass2");

// Spans de los requisitos visuales
const reqLength = document.getElementById("req-length");
const reqUppercase = document.getElementById("req-uppercase");

// Mensajes
const mismatchMsg = document.getElementById("password-error");      // "Las contraseñas no coinciden..."
const reqMsg = document.getElementById("password-req-error");       // Mensaje dinámico de requisitos

function setReqVisual(okNode, ok) {
  if (ok) {
    okNode.innerHTML = '<i class="bi bi-check-circle-fill text-success"></i>';
  } else {
    okNode.innerHTML = '<i class="bi bi-x-circle text-danger"></i>';
  }
}


function resetReqVisualsToDefault() {
  setReqVisual(reqLength, false);
  setReqVisual(reqUppercase, false);
}

// Actualiza los requisitos mientras el usuario escribe (feedback en vivo)
function updateRequirementsLive() {
  const v = pass1.value || "";
  const lengthOK = v.length >= 6;
  const upperOK = /[A-Z]/.test(v);

  setReqVisual(reqLength, lengthOK);
  setReqVisual(reqUppercase, upperOK);

  return { lengthOK, upperOK };
}

// Feedback en vivo al escribir en la contraseña
pass1.addEventListener("input", function() {
  updateRequirementsLive();
  // Si el usuario empieza a escribir otra vez → ocultamos el mensaje de requisitos
  reqMsg.style.display = "none";
  reqMsg.innerHTML = "";
});

// Validación al ENVIAR (click en Registrar)
form.addEventListener("submit", function (event) {
  // Oculta mensajes previos
  mismatchMsg.style.display = "none";
  reqMsg.style.display = "none";
  reqMsg.innerHTML = "";

  // Asegura que los checks estén actualizados a lo último escrito
  const { lengthOK, upperOK } = updateRequirementsLive();

  // 1) Primero validamos REQUISITOS de contraseña
  if (!lengthOK || !upperOK) {
    event.preventDefault(); // no envía
    // Construimos un mensaje claro debajo de los requisitos
    const faltantes = [];
    if (!lengthOK) faltantes.push("• Al menos 6 caracteres");
    if (!upperOK) faltantes.push("• Al menos 1 letra mayúscula");

    reqMsg.innerHTML = "La contraseña no cumple los requisitos:<br>" + faltantes.join("<br>");
    reqMsg.style.display = "block";

    // Limpiamos solo contraseñas y reseteamos checks a rojo
    pass1.value = "";
    pass2.value = "";
    resetReqVisualsToDefault();
    pass1.focus();
    return;
  }

  // 2) Luego validamos que ambas contraseñas COINCIDAN
  if (pass1.value !== pass2.value) {
    event.preventDefault(); // no envía
    mismatchMsg.style.display = "block";

    // Limpiamos solo contraseñas y reseteamos checks a rojo
    pass1.value = "";
    pass2.value = "";
    resetReqVisualsToDefault();
    pass1.focus();
    return;
  }

  // Si pasa ambos, se envía normalmente
});

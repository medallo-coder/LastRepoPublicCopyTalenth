console.log('🔄 mensajeria.js inicializado');

const socket = io();
const userId = +document.getElementById('currentUserId').value;
const chatPartnerInicial = +document.getElementById('chatPartnerInicial')?.value || null;
let chatPartner = null;
let chatAbiertoPorSession = false;

socket.emit('identify', { user_id: userId });

/* =========================
   FUNCIONES DE MENSAJERÍA
========================= */

function scrollToBottom() {
  const chatContainer = document.getElementById('chatContainer');
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function renderMessage(m) {
  const div = document.createElement('div');
  div.classList.add('message', m.emisor === userId ? 'sent' : 'received');
  if (m.leido && m.emisor === userId) div.classList.add('read');
  div.dataset.mensajeId = m.mensaje_id;

  const textP = document.createElement('p');
  textP.textContent = m.texto;
  div.appendChild(textP);

  const meta = document.createElement('span');
  meta.className = 'timestamp';

  const hora = document.createElement('span');
  hora.textContent = new Date(m.fecha).toLocaleTimeString();
  meta.appendChild(hora);

  if (m.emisor === userId) {
    const visto = document.createElement('span');
    visto.className = 'visto';
    visto.textContent = m.leido ? '✔✔' : '✔';
    meta.appendChild(visto);
  }

  div.appendChild(meta);
  return div;
}

function refreshConversations() {
  fetch(`/mensajeria/conversaciones/${userId}`)
    .then(res => res.json())
    .then(users => {
      const panel = document.getElementById('conversationsPanel');
      panel.innerHTML = '';

      users.forEach(u => {
        const div = document.createElement('div');
        div.className = 'conversation';
        div.dataset.userId = u.usuario_id;

        div.innerHTML = `
          <div class="left">
            <img src="/static/uploads/${u.foto}" alt="Perfil" />
            <div>
              <h2>${u.nombre}</h2>
              <small>${u.ultimo_texto}</small>
            </div>
          </div>
          <div class="right">
            <!-- Botón menú -->
            <div class="menu-button-container">
             <button class="menu-btn"><i class="bi bi-three-dots"></i></button>
              <div class="contact-menu oculto">
                <span class="menu-close-btn">&times;</span>
                <a href="javascript:void(0);" class="abrir-modal-calificacion">
                  <i class="bi bi-star"></i><span>Calificar</span>
                </a>
                <a href="javascript:void(0);" class="btn-link abrir-modal-reporte">
                 <i class="bi bi-exclamation-circle"></i><span>Reportar</span>
                </a>
                <a href="#"><i class="bi bi-trash"></i><span>Eliminar</span></a>
              </div>
            </div>
            <span class="time">${u.hora}</span>
            <div class="badge" style="${u.pendientes > 0 ? '' : 'display: none;'}">${u.pendientes}</div>
          </div>
        `;

        const handleClick = () => {
          chatPartner = u.usuario_id;
          document.getElementById('chatUserName').textContent = u.nombre;
          document.getElementById('chatProfilePhoto').src = `/static/uploads/${u.foto}`;
          document.getElementById('chatContainer').innerHTML = '';
          socket.emit('join_chat', { user_id: userId, other_user_id: chatPartner });
          refreshConversations();
        };

        div.querySelector('.left').addEventListener('click', handleClick);
        panel.appendChild(div);

        // Si viene con sesión abierta
        if (chatPartnerInicial && u.usuario_id === chatPartnerInicial && !chatAbiertoPorSession) {
          chatAbiertoPorSession = true;
          handleClick();
        }
      });
    });
}

refreshConversations();

/* =========================
   SOCKET.IO EVENTOS
========================= */

socket.on('chat_history', msgs => {
  const c = document.getElementById('chatContainer');
  c.innerHTML = '';
  msgs.forEach(m => {
    c.appendChild(renderMessage(m));
    if (m.id_receptor === userId && !m.leido) {
      socket.emit('message_seen', { mensaje_id: m.mensaje_id, user_id: userId });
    }
  });
  setTimeout(scrollToBottom, 50);
});

function sendMessage() {
  const inp = document.getElementById('messageInput');
  const texto = inp.value.trim();
  if (!texto || !chatPartner) return;

  socket.emit('send_message', {
    user_id: userId,
    other_user_id: chatPartner,
    texto: texto
  });

  inp.value = '';
  refreshConversations();
}

document.getElementById('sendBtn').addEventListener('click', sendMessage);
document.getElementById('messageInput').addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    e.preventDefault();
    sendMessage();
  }
});

socket.on('new_message', m => {
  const c = document.getElementById('chatContainer');
  if (!c) return;

  const esReceptor = m.receptor === userId;
  const esEmisor = m.emisor === userId;
  const esDelChatActivo =
    (m.emisor === chatPartner && m.receptor === userId) ||
    (m.receptor === chatPartner && m.emisor === userId);

  if (esDelChatActivo) {
    c.appendChild(renderMessage(m));
    setTimeout(scrollToBottom, 50);

    if (esReceptor) {
      socket.emit('message_seen', { mensaje_id: m.mensaje_id, user_id: userId });
      refreshConversations();
    } else if (esEmisor) {
      refreshConversations();
    }
  } else {
    refreshConversations();
  }
});

socket.on('message_read', data => {
  const ids = Array.isArray(data.mensaje_id) ? data.mensaje_id : [data.mensaje_id];
  ids.forEach(id => {
    const msgDiv = document.querySelector(`[data-mensaje-id="${id}"]`);
    if (!msgDiv) return;

    msgDiv.classList.add('read');
    let visto = msgDiv.querySelector('.visto');
    if (!visto) {
      visto = document.createElement('span');
      visto.className = 'visto';
      msgDiv.appendChild(visto);
    }
    visto.textContent = '✔✔';
    visto.style.color = '#4fc3f7';
  });

  refreshConversations();
});

socket.on('update_conversations', () => {
  refreshConversations();
});

/* =========================
   MENÚ CONTEXTUAL (3 puntos)
   Compatible con .menu-btn + .contact-menu
========================= */
document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('click', function (e) {
    // 1️⃣ Si hace clic en el botón de los tres puntos
    const menuBtn = e.target.closest('.menu-btn');
    if (menuBtn) {
      const rightCol = menuBtn.closest('.right');
      const menu = rightCol?.querySelector('.contact-menu');
      if (!menu) return;

      // Cerrar otros menús
      document.querySelectorAll('.contact-menu').forEach(m => {
        if (m !== menu) m.classList.add('oculto');
      });

      // Mostrar/ocultar este
      menu.classList.toggle('oculto');
      e.stopPropagation();
      return;
    }

    // 2️⃣ Si hace clic dentro del menú en uno de sus botones
    const menuActionBtn = e.target.closest('.contact-menu button');
    if (menuActionBtn) {
      const action = menuActionBtn.textContent.trim();
      console.log('Acción del menú:', action);
      menuActionBtn.closest('.contact-menu').classList.add('oculto');
      return;
    }

    // 3️⃣ Clic fuera → cerrar todos los menús
    document.querySelectorAll('.contact-menu').forEach(m => m.classList.add('oculto'));
  });

  // === DELEGACIÓN para abrir y cerrar el modal de calificación ===
document.addEventListener("click", (e) => {
  // Abrir modal (cuando se haga clic en un enlace con la clase .abrir-modal-calificacion)
  if (e.target.closest(".abrir-modal-calificacion")) {
    const modal = document.getElementById("modalCalificacion");
    modal.style.display = "flex";
  }

  // Cerrar modal (botón cancelar)
  if (e.target.id === "cancelarModalCalificacion") {
    const modal = document.getElementById("modalCalificacion");
    modal.style.display = "none";
  }

  // Cerrar modal si se hace clic fuera del contenido
  const modal = document.getElementById("modalCalificacion");
  if (e.target === modal) {
    modal.style.display = "none";
  }
});

// === DELEGACIÓN para abrir y cerrar el modal de eliminar ===
document.addEventListener("click", (e) => {
  // Abrir modal al hacer clic en “Eliminar”
  if (e.target.closest(".contact-menu a") && e.target.closest("a").textContent.includes("Eliminar")) {
    const modal = document.getElementById("confirmModal");
    modal.style.display = "flex";
  }

  // Cerrar modal al hacer clic en “Cancelar”
  if (e.target.id === "cancelDelete") {
    const modal = document.getElementById("confirmModal");
    modal.style.display = "none";
  }

  // Cerrar modal si se hace clic fuera del contenido
  const modal = document.getElementById("confirmModal");
  if (e.target === modal) {
    modal.style.display = "none";
  }

  // El botón “Aceptar” no hace nada (aún)
  if (e.target.id === "confirmDelete") {
    console.log("🗑️ Confirmar eliminar — función aún no implementada");
    modal.style.display = "none";
  }
});

 const estrellas = document.querySelectorAll("#estrellasCalificacion i");
  let calificacion = 0;

  estrellas.forEach((estrella) => {
    estrella.addEventListener("mouseenter", () => {
      const valor = parseInt(estrella.dataset.valor);
      pintarEstrellas(valor);
    });

    estrella.addEventListener("mouseleave", () => {
      pintarEstrellas(calificacion);
    });

    estrella.addEventListener("click", () => {
      calificacion = parseInt(estrella.dataset.valor);
      console.log("⭐ Calificación seleccionada:", calificacion);
    });
  });

  function pintarEstrellas(valor) {
    estrellas.forEach((estrella) => {
      if (parseInt(estrella.dataset.valor) <= valor) {
        estrella.classList.add("activa");
        estrella.classList.remove("bi-star"); 
        estrella.classList.add("bi-star-fill"); // llena la estrella
      } else {
        estrella.classList.remove("activa");
        estrella.classList.remove("bi-star-fill");
        estrella.classList.add("bi-star"); // vacía la estrella
      }
    });
  }
  
});



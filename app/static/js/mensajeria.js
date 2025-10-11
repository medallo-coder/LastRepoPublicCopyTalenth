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
  hora.textContent = new Date(m.fecha).toLocaleTimeString('es-CO', {
  hour: 'numeric',
  minute: '2-digit',
  hour12: true
  });

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
      const sidebar = document.querySelector('.chat-sidebar');
      const placeholder = document.getElementById('chatPlaceholder');
      const chatContent = document.getElementById('chatContent');

      // Si no hay conversaciones
      if (users.length === 0) {
        sidebar.style.display = 'none';
        placeholder.innerHTML = `
          <p>Aún no tienes conversaciones.</p>
          <p>¡Contacta a un experto para comenzar!</p>
          <a href="/publicaciones" class="btn-explorar">Explorar expertos</a>
        `;
        placeholder.classList.remove('oculto');
        chatContent.classList.add('oculto');
      } else {
        sidebar.style.display = 'block';
      }




      users.forEach(u => {
        const div = document.createElement('div');
        div.className = 'conversation';
        div.dataset.userId = u.usuario_id;
        

        let fotoHTML = '';
          if (u.foto && u.foto !== 'default.jpg') {
            // Si la ruta ya viene completa (por ejemplo /uploads/perfiles/archivo.jpg)
            // úsala directamente; si solo viene el nombre, la completamos
            const fotoSrc = u.foto.startsWith('/uploads/')
              ? u.foto
              : `/uploads/perfiles/${u.foto.replace(/^\/+/, '')}`;
            fotoHTML = `<img src="${fotoSrc}" alt="Foto de perfil" class="perfil-img">`;
          } else {
            fotoHTML = `<i class="bi bi-person-circle perfil-img placeholder-icon"></i>`;
          }



        div.innerHTML = `
          <div class="left">
            ${fotoHTML}
            <div>
              <h2>${u.nombre}</h2>
              <small>${u.ultimo_texto || ''}</small>
            </div>
          </div>
          <div class="right">
            <div class="menu-button-container">
              <button class="menu-btn"><i class="bi bi-three-dots"></i></button>
              <div class="contact-menu oculto">
                <span class="menu-close-btn">&times;</span>
                <a href="javascript:void(0);" class="abrir-modal-calificacion">
                  <i class="bi bi-star"></i><span>Calificar</span>
                </a>
                <a href="javascript:void(0);"
                  class="btn-link abrir-modal-reporte"
                  data-usuario-reportado="${u.usuario_id}"
                  data-usuario-reportador="${userId}">
                  <i class="bi bi-exclamation-circle"></i><span>Reportar</span>
                </a>
                <a href="#"><i class="bi bi-trash"></i><span>Eliminar</span></a>
              </div>
            </div>
            <span class="time">${u.hora || ''}</span>
            <div class="badge" style="${u.pendientes > 0 ? '' : 'display:none;'}">${u.pendientes || ''}</div>
          </div>
        `;

        
        const handleClick = () => {
          chatPartner = u.usuario_id;
          document.getElementById('chatPlaceholder').classList.add('oculto');
          document.getElementById('chatContent').classList.remove('oculto');
          document.getElementById('chatUserName').textContent = u.nombre;

          const chatPhoto = document.getElementById('chatProfilePhoto');
          const chatIcon = document.querySelector('.profile .placeholder-icon');

          if (u.foto && u.foto !== 'default.jpg') {
            const fotoSrc = u.foto.startsWith('/uploads/')
              ? u.foto
              : `/uploads/perfiles/${u.foto.replace(/^\/+/, '')}`;
            chatPhoto.src = fotoSrc;
            chatPhoto.classList.remove('oculto');
            chatIcon.classList.add('oculto');
          } else {
            chatPhoto.classList.add('oculto');
            chatIcon.classList.remove('oculto');
          }

          document.getElementById('chatContainer').innerHTML = '';
          socket.emit('join_chat', { user_id: userId, other_user_id: chatPartner });
          refreshConversations();

          // ✅ Responsive móvil
          const chatPanel = document.getElementById('chatPanel');
          const backBtn = document.getElementById('backButton');
          if (window.innerWidth <= 768) {
            chatPanel.classList.add('active');
            document.querySelector('.chat-sidebar').style.display = 'none';
            backBtn.classList.remove('oculto');
          }
        };

        div.querySelector('.left').addEventListener('click', handleClick);
        panel.appendChild(div);

        // Abrir si viene por sesión
        if (chatPartnerInicial && u.usuario_id === chatPartnerInicial && !chatAbiertoPorSession) {
          chatAbiertoPorSession = true;
          handleClick();
        }
      });
    });
}

refreshConversations();
// --- BOTÓN "VER PERFIL" ---
document.getElementById("viewProfileBtn").addEventListener("click", () => {
  if (!chatPartner) {
    alert("Selecciona primero un chat para ver el perfil del usuario.");
    return;
  }

  // Redirige al endpoint que decide si es experto o cliente
  window.location.href = `/mensajeria/ver_perfil/${chatPartner}`;
});


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
  const menuBtn = e.target.closest('.menu-btn');
  if (menuBtn) {
    let menu = menuBtn.__menuRef; // ← recuperar si ya existe

    // Si no existe, buscarlo una vez y guardarlo
    if (!menu) {
      menu = menuBtn.parentElement.querySelector('.contact-menu');
      if (!menu) return;
      menuBtn.__menuRef = menu; // guardar referencia
    }

    // Mover el menú al body una sola vez
    if (!menu.__movedToBody) {
      document.body.appendChild(menu);
      menu.__movedToBody = true;
    }

    // Cerrar otros menús
    document.querySelectorAll('.contact-menu').forEach(m => {
      if (m !== menu) m.classList.add('oculto');
    });

    // Alternar visibilidad
    const isHidden = menu.classList.contains('oculto');
    if (isHidden) {
      menu.classList.remove('oculto');
      const rect = menuBtn.getBoundingClientRect();
      const menuWidth = 140;
      const menuHeight = menu.offsetHeight || 100;
      let top = rect.bottom + 6;
      let left = rect.right - menuWidth;

      // Asegura que no se salga de la pantalla
      if (top + menuHeight > window.innerHeight) top = rect.top - menuHeight - 6;
      if (left < 0) left = 8;

      Object.assign(menu.style, {
        position: 'fixed',
        top: `${top}px`,
        left: `${left}px`,
        display: 'flex',
        zIndex: 999999
      });
    } else {
      menu.classList.add('oculto');
    }

    e.stopPropagation();
    return;
  }

  // Clic fuera → cerrar todos los menús
  if (!e.target.closest('.contact-menu')) {
    document.querySelectorAll('.contact-menu').forEach(m => m.classList.add('oculto'));
  }

  // === Ajustar altura dinámica del textarea ===
const textarea = document.getElementById('messageInput');
if (textarea) {
  textarea.addEventListener('input', () => {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 60) + 'px'; // crece hasta 120px
  });
}

});


// === DELEGACIÓN para abrir y cerrar el modal de calificación ===
document.addEventListener("click", (e) => {
  // Abrir modal (cuando se haga clic en un enlace con la clase .abrir-modal-calificacion)
  if (e.target.closest(".abrir-modal-calificacion")) {
    const modal = document.getElementById("modalCalificacion");
    modal.style.display = "flex";

    // 🔹 Cerrar cualquier menú contextual abierto
    document.querySelectorAll(".contact-menu").forEach(m => m.classList.add("oculto"));
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

// --- ENVÍO DE CALIFICACIÓN POR AJAX ---
const formCalificacion = document.getElementById("formCalificacion");

if (formCalificacion) {
  formCalificacion.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(formCalificacion);

    try {
      const res = await fetch(formCalificacion.action, {
        method: "POST",
        body: formData
      });

      const data = await res.json();

      // Mostrar mensaje dinámico
      mostrarMensaje(data.message, data.success ? "success" : "danger");

      if (data.success) {
        // Cerrar modal y limpiar formulario
        const modal = document.getElementById("modalCalificacion");
        if (modal) modal.style.display = "none";
        formCalificacion.reset();
        const inputValor = document.getElementById("valorCalificacion");
        if (inputValor) inputValor.value = 0;

        // Opcional: refrescar lista de conversaciones o perfil
        refreshConversations();
      }

    } catch (err) {
      console.error(err);
      mostrarMensaje("Error al enviar la calificación", "danger");
    }
  });
}

// Función para mostrar alertas temporales
function mostrarMensaje(msg, tipo) {
  const container = document.querySelector(".messages-container") || document.body;
  const div = document.createElement("div");
  div.className = `alert ${tipo}`;
  div.textContent = msg;
  container.prepend(div);
  setTimeout(() => div.remove(), 4000);
}


// === DELEGACIÓN para abrir y cerrar el modal de eliminar ===
document.addEventListener("click", (e) => {
  // Abrir modal al hacer clic en “Eliminar”
  if (e.target.closest(".contact-menu a") && e.target.closest("a").textContent.includes("Eliminar")) {
    const modal = document.getElementById("confirmModal");
    modal.style.display = "flex";

    // 🔹 Cerrar cualquier menú contextual abierto
    document.querySelectorAll(".contact-menu").forEach(m => m.classList.add("oculto"));
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
      // ✅ NUEVO: actualizar campo oculto del formulario
    const inputValor = document.getElementById("valorCalificacion");
    if (inputValor) inputValor.value = calificacion;
      
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

// 🔹 Cuando el usuario selecciona una conversación
function abrirChat(otroUsuarioId) {
  const chatPanel = document.getElementById("chatPanel");
  chatPanel.dataset.partnerId = otroUsuarioId;
  console.log("💬 Chat abierto con usuario:", otroUsuarioId);
}

document.addEventListener("click", (e) => {
  const btn = e.target.closest(".abrir-modal-calificacion");
  if (!btn) return;

  // buscar la conversación donde se hizo clic
  const conversation = btn.closest(".conversation");
  const usuarioId = conversation?.dataset.userId;
  const input = document.getElementById("calificadoId");

  if (usuarioId && input) {
    input.value = usuarioId;
    console.log("✅ Calificado ID asignado desde conversación:", usuarioId);
  } else {
    console.warn("⚠️ No se pudo asignar calificado_id");
  }

  // mostrar modal
  const modal = document.getElementById("modalCalificacion");
  if (modal) modal.style.display = "flex";
});



// Cerrar menú al hacer clic en la "X"
document.addEventListener('click', (e) => {
  const closeBtn = e.target.closest('.menu-close-btn');
  if (closeBtn) {
    const menu = closeBtn.closest('.contact-menu');
    if (menu) {
      menu.classList.add('oculto');
    }
  }
});
// ICONO < ATRÁS (junto a la foto)
const backIcon = document.getElementById('backIcon');
if (backIcon) {
  backIcon.addEventListener('click', () => {
    // Ocultar panel de chat (mobile)
    const chatPanel = document.getElementById('chatPanel');
    chatPanel.classList.remove('active');

    // Mostrar sidebar de conversaciones
    const sidebar = document.querySelector('.chat-sidebar');
    if (sidebar) sidebar.style.display = 'block';

    // Ocultar el icono de regreso si quieres (opcional)
    // backIcon.classList.add('oculto');

    // Ocultar contenido del chat
    const chatContent = document.getElementById('chatContent');
    if (chatContent) chatContent.classList.add('oculto');

    // Mostrar placeholder
    const chatPlaceholder = document.getElementById('chatPlaceholder');
    if (chatPlaceholder) chatPlaceholder.classList.remove('oculto');

    // Limpiar chat seleccionado
    chatPartner = null;
  });
}

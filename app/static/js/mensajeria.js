// static/js/mensajeria.js
console.log('🔄 mensajeria.js inicializado');

const socket = io(); // conecta al mismo origen
const userId = +document.getElementById('currentUserId').value;
socket.emit('identify', { user_id: userId }); // 🟢 Identifica al usuario al conectarse
let chatPartner = null;

function scrollToBottom() {
  const chatContainer = document.getElementById('chatContainer');
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Función para renderizar un mensaje con timestamp y visto
function renderMessage(m) {
  const div = document.createElement('div');
  div.classList.add('message', m.emisor === userId ? 'sent' : 'received');
  if (m.leido && m.emisor === userId) div.classList.add('read');
  div.dataset.mensajeId = m.mensaje_id;

  // Texto
  const textP = document.createElement('p');
  textP.textContent = m.texto;
  div.appendChild(textP);

  // Contenedor de hora + visto
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
        div.innerHTML = `
        <div class="left">
            <img src="/static/uploads/${u.foto}" alt="Perfil" />
            <div>
              <h2>${u.nombre}</h2>
              <small>${u.ultimo_texto}</small>
            </div>
          </div>
          <div class="right">
            <button class="menu-btn"><i class="bi bi-three-dots"></i></button>
            <span class="time">${u.hora}</span>
            <div class="badge" style="${u.pendientes > 0 ? '' : 'display: none;'}">${u.pendientes}</div>
            <div class="contact-menu oculto">
              <!-- opciones -->
            </div>
          </div>
        `;

        div.querySelector('.left').onclick = () => {
          chatPartner = u.usuario_id;
          document.getElementById('chatUserName').textContent = u.nombre;
          document.getElementById('chatProfilePhoto').src = `/static/uploads/${u.foto}`;
          document.getElementById('chatContainer').innerHTML = '';
          socket.emit('join_chat', { user_id: userId, other_user_id: chatPartner });
          refreshConversations();
        };

        panel.appendChild(div);
      });
    });
}

refreshConversations();
// 2) Recibe e imprime historial
socket.on('chat_history', msgs => {
  const c = document.getElementById('chatContainer');
  c.innerHTML = '';
  msgs.forEach(m => {
    c.appendChild(renderMessage(m));
    // Si es mensaje recibido y no estaba leído, avisar al servidor
    if (m.id_receptor === userId && !m.leido) {
      socket.emit('message_seen', { mensaje_id: m.mensaje_id, user_id: userId });
    }
  });
  setTimeout(() => {
    c.scrollTop = c.scrollHeight;
  }, 50);
  requestAnimationFrame(scrollToBottom);
});

// 3) Enviar mensaje
function sendMessage() {
  const inp = document.getElementById('messageInput');
  const texto = inp.value.trim();
  if (!texto || !chatPartner) return;

  console.log("Enviando mensaje:", texto); // ← ahora sí funciona

  socket.emit('send_message', {
    user_id: userId,
    other_user_id: chatPartner,
    texto: texto
  });
  refreshConversations(); // ← resalta pendientes
  inp.value = '';
}


document.getElementById('sendBtn').addEventListener('click', sendMessage);
document.getElementById('messageInput').addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    e.preventDefault();
    sendMessage();
  }
});

// 4) Mostrar nuevos mensajes en tiempo real
socket.on('new_message', m => {
  console.log("📩 new_message recibido:", m);

  const c = document.getElementById('chatContainer');
  if (!c) return;

  const esReceptor     = m.receptor === userId;
  const esEmisor       = m.emisor === userId;
  const esDelChatActivo =
    (m.emisor === chatPartner && m.receptor === userId) ||
    (m.receptor === chatPartner && m.emisor === userId);

  if (esDelChatActivo) {
    console.log("🌈 Pintando mensaje en chat activo");
    c.appendChild(renderMessage(m));
    setTimeout(() => {
      c.scrollTop = c.scrollHeight;
    }, 50);

    if (esReceptor) {
      socket.emit('message_seen', { mensaje_id: m.mensaje_id, user_id: userId });
      refreshConversations(); // 👈 al leerlo, baja el contador
    } else if (esEmisor) {
      refreshConversations(); // 👈 actualiza lista (orden/último mensaje)
    }
  } else {
    console.log("🔔 Mensaje fuera del chat activo");
    refreshConversations(); // 👈 sube contador
  }
  requestAnimationFrame(scrollToBottom);
});

// 5) Escuchar confirmación de lectura
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

  console.log("🔄 Refrescando conversaciones tras lectura");
  refreshConversations(); // 👈 Forzar actualización de pendientes
});


socket.on('update_conversations', () => {
  console.log("🔄 Actualizando lista de conversaciones por evento remoto");
  refreshConversations();
});



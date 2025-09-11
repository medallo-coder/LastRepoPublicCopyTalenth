console.log('🔄 mensajeria.js inicializado');

const socket = io();
const userId = +document.getElementById('currentUserId').value;
const chatPartnerInicial = +document.getElementById('chatPartnerInicial')?.value || null;
let chatPartner = null;
let chatAbiertoPorSession = false;

socket.emit('identify', { user_id: userId });

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
            <button class="menu-btn"><i class="bi bi-three-dots"></i></button>
            <span class="time">${u.hora}</span>
            <div class="badge" style="${u.pendientes > 0 ? '' : 'display: none;'}">${u.pendientes}</div>
            <div class="contact-menu oculto"></div>
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

        // Solo abrir si venimos con session y aún no lo hicimos
        if (chatPartnerInicial && u.usuario_id === chatPartnerInicial && !chatAbiertoPorSession) {
          chatAbiertoPorSession = true;
          handleClick();
        }
      });
    });
}

refreshConversations();

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

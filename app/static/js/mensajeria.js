// static/js/mensajeria.js
console.log('🔄 mensajeria.js inicializado');

const socket = io();            // conecta al mismo origen
const userId = +document.getElementById('currentUserId').value;
let chatPartner = null;

// 1) Carga lista de usuarios
fetch('/mensajeria/usuarios')
  .then(res => res.json())
  .then(users => {
    const ul = document.getElementById('conversationsList');
    ul.innerHTML = '';
    users.forEach(u => {
      const li = document.createElement('li');
      li.textContent = u.nombre;
      li.dataset.id = u.usuario_id;
      li.onclick = () => {
        chatPartner = u.usuario_id;
        socket.emit('join_chat', { user_id: userId, other_user_id: chatPartner });
      };
      ul.appendChild(li);
    });
  });

// 2) Recibe e imprime historial
socket.on('chat_history', msgs => {
  const c = document.getElementById('chatContainer');
  c.innerHTML = '';
  msgs.forEach(m => {
    const who = m.emisor === userId ? 'Tú' : 'Ellos';
    const div = document.createElement('div');
    div.textContent = `[${new Date(m.fecha_chat).toLocaleTimeString()}] ${who}: ${m.texto}`;
    c.appendChild(div);
  });
});

// 3) Enviar mensaje
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
  // 1) Referencia al contenedor
  const c = document.getElementById('chatContainer');

  // 2) Crea el wrapper del mensaje
  const div = document.createElement('div');
  div.className = m.emisor === userId ? 'sent' : 'received';

  // 3) Inserta el texto
  div.textContent = m.texto;

  // 4) (Opcional) Añade un timestamp
   const ts = document.createElement('span');
   ts.className = 'timestamp';
   ts.textContent = new Date(m.fecha_chat).toLocaleTimeString();
   div.appendChild(ts);

  // 5) Mete el mensaje en el DOM y haz scroll
  c.appendChild(div);
  c.scrollTop = c.scrollHeight;
});

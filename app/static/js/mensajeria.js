document.addEventListener('DOMContentLoaded', async () => {
    await loadUsers();
    await loadConversations();
});

document.getElementById('goHomeBtn').addEventListener('click', () => {
    window.location.href = '/';
});

const currentUserElement = document.getElementById('currentUserId');
if (!currentUserElement) {
    console.error("Error: No se encontró el ID de usuario actual.");
}
const currentUserId = currentUserElement.value;
const conversationsList = document.getElementById('conversationsList');
const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendMessageBtn = document.getElementById('sendMessageBtn');
let selectedUserId = null;

// Enviar con Enter
messageInput.addEventListener('keydown', async (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        await sendMessage();
    }
});

// También puedes usar el botón
sendMessageBtn.addEventListener('click', sendMessage);

async function loadUsers() {
    try {
        const res = await fetch('/mensajeria/usuarios');
        const users = await res.json();
        conversationsList.innerHTML = '';
        users.forEach(user => {
            const li = document.createElement('li');
            li.classList.add('user-item');
            li.dataset.userid = user.usuario_id;
            li.innerHTML = `
                <img src="/static/uploads/${user.foto}" alt="foto" class="user-photo">
                <span>${user.nombre}</span>
            `;
            li.addEventListener('click', () => {
                document.querySelectorAll('.user-item').forEach(el => el.classList.remove('active'));
                li.classList.add('active');
                selectedUserId = user.usuario_id;
                document.getElementById('chatUserName').innerText = user.nombre;
                document.getElementById('chatProfilePhoto').src = `/static/uploads/${user.foto}`;
                loadMessages(currentUserId, selectedUserId);
            });
            conversationsList.appendChild(li);
        });
    } catch (err) {
        console.error("Error cargando usuarios:", err);
    }
}

async function loadConversations() {
    try {
        const res = await fetch(`/mensajeria/conversaciones/${currentUserId}`);
        const data = await res.json();
        // Aquí podrías agregar notificaciones, resumen de últimos mensajes, etc.
    } catch (err) {
        console.error("Error cargando conversaciones:", err);
    }
}

async function loadMessages(idEmisor, idReceptor) {
    try {
        const res = await fetch(`/mensajeria/${idEmisor}/${idReceptor}`);
        const mensajes = await res.json();
        chatContainer.innerHTML = '';
        mensajes.forEach(m => {
            const div = document.createElement('div');
            div.classList.add('mensaje', m.id_emisor == currentUserId ? 'enviado' : 'recibido');
            div.innerHTML = `
                <p>${m.texto}</p>
                <span>${m.fecha}</span>
            `;
            chatContainer.appendChild(div);
        });
        chatContainer.scrollTop = chatContainer.scrollHeight;
    } catch (err) {
        console.error("Error cargando mensajes:", err);
    }
}

async function sendMessage() {
    const texto = messageInput.value.trim();
    if (!texto || !selectedUserId) return;

    const body = {
        id_emisor: currentUserId,
        id_receptor: selectedUserId,
        texto
    };

    const res = await fetch('/mensajeria/enviar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });

    if (res.ok) {
        messageInput.value = '';
        loadMessages(currentUserId, selectedUserId);
    }
}

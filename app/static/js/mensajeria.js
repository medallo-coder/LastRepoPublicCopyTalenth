document.addEventListener('DOMContentLoaded', async () => {
    await loadUsers(); // Primero carga todos los usuarios
    await loadConversations(); // Luego carga conversaciones sin eliminar usuarios
});

document.getElementById('goHomeBtn').addEventListener('click', () => {
    window.location.href = '/'; // Redirecciona al inicio
});


const currentUserIdElement = document.getElementById('currentUserId');
if (!currentUserIdElement) {
    console.error("Error: No se encontró el ID de usuario actual.");
}
const currentUserId = currentUserIdElement.value;
const conversationsList = document.getElementById('conversationsList');
const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendMessageBtn = document.getElementById('sendMessageBtn');
const chatUserName = document.getElementById('chatUserName');

let selectedUserId = null;

// Cargar historial de mensajes al seleccionar una conversación
conversationsList.addEventListener('click', e => {
    const conversationItem = e.target.closest('.conversation-item');
    if (conversationItem) {
        selectedUserId = conversationItem.dataset.userId;
        chatUserName.textContent = conversationItem.dataset.userEmail;
        loadMessages(selectedUserId);
    }
});

// Enviar mensaje
sendMessageBtn.addEventListener('click', async () => {
    const text = messageInput.value.trim();
    if (!selectedUserId || !text) return;

    try {
        const response = await fetch('/mensajeria/enviar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_emisor: currentUserId,
                id_receptor: selectedUserId,
                texto: text
            })
        });

        if (!response.ok) {
            const result = await response.json();
            alert(result.error);
            return;
        }

        messageInput.value = '';
        loadMessages(selectedUserId);
    } catch (error) {
        console.error("Error al enviar el mensaje:", error);
    }
});

// Función para cargar usuarios sin eliminarlos entre recargas
async function loadUsers() {
    try {
        const response = await fetch('/mensajeria/usuarios');
        if (!response.ok) throw new Error("Error al cargar usuarios");

        const users = await response.json();
        console.log("Usuarios cargados:", users);

        conversationsList.innerHTML = ''; // Limpiar lista antes de agregar nuevos usuarios

        users.forEach(user => {
            const div = document.createElement('div');
            div.classList.add('conversation-item');
            div.dataset.userId = user.usuario_id;
            div.dataset.userEmail = user.correo;
            div.innerHTML = `<strong>${user.correo}</strong>`;

            // Evento para abrir conversación al hacer clic
            div.addEventListener('click', () => {
                selectedUserId = user.usuario_id;
                chatUserName.textContent = user.correo;
                loadMessages(selectedUserId);
            });

            conversationsList.appendChild(div);
        });

        console.log("Usuarios insertados en el HTML:", conversationsList.children.length);

    } catch (error) {
        console.error("Error cargando usuarios:", error);
    }
}

// Función para actualizar solo conversaciones sin borrar usuarios
async function loadConversations() {
    try {
        const currentUserId = document.getElementById('currentUserId').value;
        if (!currentUserId) {
            console.error("Error: `currentUserId` no está definido.");
            return;
        }

        const response = await fetch(`/mensajeria/conversaciones/${currentUserId}`);
        if (!response.ok) throw new Error("Error al cargar conversaciones");

        const conversations = await response.json();
        console.log("Conversaciones cargadas:", conversations);

        conversations.forEach(convo => {
            const userElement = document.querySelector(`[data-user-id="${convo.usuario_id}"]`);
            if (userElement) {
                userElement.innerHTML += `<small>${convo.ultimo_mensaje}</small>`;
            }
        });

    } catch (error) {
        console.error("Error cargando conversaciones:", error);
    }
}

// Función para cargar historial de mensajes
async function loadMessages(userId) {
    try {
        const chatPanel = document.querySelector('.chat-panel'); // Obtener el panel de chat
        chatPanel.style.display = 'flex'; // Mostrar el panel

        const response = await fetch(`/mensajeria/${currentUserId}/${userId}`);
        if (!response.ok) throw new Error("Error al cargar mensajes");

        const data = await response.json();
        chatContainer.innerHTML = '';

        data.forEach(msg => {
            const div = document.createElement('div');
            div.classList.add('message');
            div.classList.add(msg.id_emisor == currentUserId ? 'sent' : 'received');
            div.innerHTML = `
                <p>${msg.texto}</p>
                <span>${msg.fecha}</span>
            `;
            chatContainer.appendChild(div);
        });

        chatContainer.scrollTop = chatContainer.scrollHeight;
    } catch (error) {
        console.error("Error cargando mensajes:", error);
    }
}

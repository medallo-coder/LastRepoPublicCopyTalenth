
        // Desaparecer los mensajes después de 3 segundos
        setTimeout(function() {
            const messages = document.querySelectorAll('.alert');
            messages.forEach(message => {
                message.style.opacity = '0';
                setTimeout(() => message.remove(), 500); // Remover tras la animación
            });
        }, 3000);
document.addEventListener('DOMContentLoaded', function() {
    const messagesDiv = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    function addMessage(text, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', isUser ? 'user' : 'bot');
        const textDiv = document.createElement('div');
        textDiv.classList.add('message-text');
        textDiv.textContent = text;
        messageDiv.appendChild(textDiv);
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        addMessage(message, true);
        userInput.value = '';

        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // if CSRF is enabled
                },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            addMessage(data.response, false);
        } catch (error) {
            console.error('Error:', error);
            addMessage('Sorry, something went wrong.', false);
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });

    // CSRF token helper (if you keep CSRF protection)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
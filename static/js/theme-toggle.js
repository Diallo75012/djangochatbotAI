// Theme Toggle Functionality
function toggleTheme() {
    // console.log("Toggle button clicked"); // For debugging
    // Toggle theme based on the current theme
    if (document.body.getAttribute("data-theme") === "dark") {
        // Switch to light mode
        document.body.setAttribute("data-theme", "light");
        localStorage.setItem("theme", "light");
    } else {
        // Switch to dark mode
        document.body.setAttribute("data-theme", "dark");
        localStorage.setItem("theme", "dark");
    }
}

// Set theme on load based on user preference
document.addEventListener("DOMContentLoaded", function () {
    // Retrieve the user's theme preference from localStorage
    const savedTheme = localStorage.getItem("theme");

    // Apply the user's saved theme preference once on page load
    if (savedTheme) {
        document.body.setAttribute("data-theme", savedTheme);
    } else {
        // Default to light theme if no preference saved
        document.body.setAttribute("data-theme", "light");
    }
});

// Ensure the theme does not unintentionally toggle when clicking other elements
document.querySelectorAll('button.toggle-theme').forEach(button => {
    button.addEventListener("click", toggleTheme);
});


// ##################################
    document.addEventListener('DOMContentLoaded', function() {
        const chatContainer = document.getElementById('chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;  // Scroll to the latest message

        const messageForm = document.getElementById('message-form');
        messageForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const messageInput = document.getElementById('message-input');
            const messageContent = messageInput.value;

            // AJAX request to post message
            fetch('/clientuserchat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}',
                },
                body: JSON.stringify({ 'message': messageContent }),
            })
            .then(response => response.json())
            .then(data => {
                // Append the user message and the bot response to the chat container
                appendMessage(chatContainer, data.user_message, 'user');
                appendMessage(chatContainer, data.bot_message, 'bot');

                // Scroll to the bottom after updating
                chatContainer.scrollTop = chatContainer.scrollHeight;
            })
            .catch(error => console.error('Error:', error));
        });
    });

    function appendMessage(container, message, sender) {
        const messageContainer = document.createElement('div');
        messageContainer.className = `message-container ${sender}-message`;

        const avatar = document.createElement('img');
        avatar.className = 'avatar';
        avatar.src = sender === 'user' ? '{{ user_avatar }}' : '{{ chatbot_avatar }}';
        avatar.alt = `${sender} avatar`;

        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';
        messageDiv.innerHTML = `<p>${message}</p>`;

        messageContainer.appendChild(avatar);
        messageContainer.appendChild(messageDiv);
        container.appendChild(messageContainer);
    }


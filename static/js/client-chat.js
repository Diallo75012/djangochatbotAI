document.addEventListener('DOMContentLoaded', function() {
  const chatContainer = document.getElementById('chat-container');
  chatContainer.scrollTop = chatContainer.scrollHeight;  // Scroll to the latest message

  const messageForm = document.getElementById('message-form');
  messageForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const messageInput = document.getElementById('message-input');
    const messageContent = messageInput.value;

    // Get the chatbot details from the sidebar
    const selectedChatbotId = document.getElementById("documentTitleDropdown").value;
    const chatbotName = document.getElementById("chatbotName")?.innerText || document.getElementById("customChatbotName")?.value;
    const chatbotAge = document.getElementById("chatbotAge")?.innerText || null;
    const chatbotOrigin = document.getElementById("chatbotOrigin")?.innerText || null;
    const chatbotDream = document.getElementById("chatbotDream")?.innerText || null;
    const chatbotTone = document.getElementById("chatbotTone")?.innerText || null;
    const chatbotDescription = document.getElementById("chatbotDescription")?.innerText || null;
    const chatbotExpertise = document.getElementById("chatbotExpertise")?.innerText || null;

    // Prepare the data to be sent to the backend
    const dataToSend = {
      'message': messageContent,
      'chatbot_id': selectedChatbotId,
      'chatbot_name': chatbotName,
      'chatbot_age': chatbotAge,
      'chatbot_origin': chatbotOrigin,
      'chatbot_dream': chatbotDream,
      'chatbot_tone': chatbotTone,
      'chatbot_description': chatbotDescription,
      'chatbot_expertise': chatbotExpertise
    };

    // AJAX request to post message and chatbot details
    fetch('/clientchat/clientuserchat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      },
      body: JSON.stringify(dataToSend),
    })
    .then(response => response.json())
    .then(data => {
      // Append the user message and the bot response to the chat container
      appendMessage(chatContainer, data.user_message, 'user');
      appendMessage(chatContainer, data.bot_message, 'bot');

      // Scroll to the bottom after updating
      chatContainer.scrollTop = chatContainer.scrollHeight;

      // Clear the message input
      messageInput.value = '';
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

// ########### SIDEBAR CLIENT CHAT CHATBOT DETAILS DYNAMIC CHANGE WHEN USER SELECT #######
document.getElementById("documentTitleDropdown").addEventListener("change", function() {
  const selectedChatbotId = this.value;

  // AJAX request to get the selected chatbot details
  fetch(`/chatbotdetails/${selectedChatbotId}/`)
    .then(response => response.json())
    .then(data => {
      if (document.getElementById("chatbotAvatar")) {
        document.getElementById("chatbotAvatar").src = data.avatar_url;
      }
      document.getElementById("chatbotAge").innerText = data.age;
      document.getElementById("chatbotOrigin").innerText = data.origin;
      document.getElementById("chatbotDream").innerText = data.dream;
      document.getElementById("chatbotName").innerText = data.name;
      document.getElementById("chatbotTone").innerText = data.tone;
      document.getElementById("chatbotDescription").innerText = data.description;
      document.getElementById("chatbotExpertise").innerText = data.expertise;
      document.getElementById("chatbotBusinessOwner").innerText = data.business_owner;
      document.getElementById("chatbotNumber").innerText = data.number;
    })
    .catch(error => console.error('Error:', error));
});


document.addEventListener('DOMContentLoaded', function() {
  const messageForm = document.getElementById('message-form');
  messageForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const messageInput = document.getElementById('message-input').value;

    // Determine if we should use default chatbot or custom fields
    let chatbotData = {};
    if (document.getElementById('chatbotName')) {
      // Default chatbot details
      chatbotData = {
        'chatbot_name': document.getElementById('chatbotName').value,
        'chatbot_age': document.getElementById('chatbotAge') ? document.getElementById('chatbotAge').value : '',
        'chatbot_origin': document.getElementById('chatbotOrigin') ? document.getElementById('chatbotOrigin').value : '',
        'chatbot_dream': document.getElementById('chatbotDream') ? document.getElementById('chatbotDream').value : '',
        'chatbot_tone': document.getElementById('chatbotTone') ? document.getElementById('chatbotTone').value : '',
        'chatbot_description': document.getElementById('chatbotDescription') ? document.getElementById('chatbotDescription').value : '',
        'chatbot_expertise': document.getElementById('chatbotExpertise') ? document.getElementById('chatbotExpertise').value : ''
      };
    } else {
      // Custom chatbot details
      chatbotData = {
        'chatbot_name': document.getElementById('customChatbotName').value || '',
        'chatbot_age': document.getElementById('customChatbotAge').value || '',
        'chatbot_origin': document.getElementById('customChatbotOrigin').value || '',
        'chatbot_dream': document.getElementById('customChatbotDream').value || '',
        'chatbot_tone': document.getElementById('customChatbotTone').value || '',
        'chatbot_description': document.getElementById('customChatbotDescription').value || '',
        'chatbot_expertise': document.getElementById('customChatbotExpertise').value || ''
      };
    }

    // Prepare data for submission
    const dataToSend = {
      'message': messageInput,
      ...chatbotData
    };

    console.log("Data to send", dataToSend);

    // AJAX request to post message
    fetch('/clientchat/clientuserchat', {
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


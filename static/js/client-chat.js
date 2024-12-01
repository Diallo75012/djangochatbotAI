// fetching sidebar data and message send from form to send it ot django backend that will process data
document.addEventListener('DOMContentLoaded', function() {
  const messageForm = document.getElementById('message-form');
  const chatContainer = document.getElementById('chat-container');
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


// chat side of webui appending messages to display those
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

// handle dropdown document_titles in sidebar. check if there is chatbotsettings associated and display detail if yes
document.getElementById("documentTitleDropdown").addEventListener("change", function() {
  // this id from business data corresponding to the document_title row will be used to fetch from the `chat_bot` field the right chatbot data
  const selectedBusinessDataId = this.value;
  console.log("Chatbot ID: ", selectedBusinessDataId, typeof(selectedBusinessDataId))

  // AJAX request to get the selected chatbot details
  fetch(`/chatbotsettings/chatbotdetails/${selectedBusinessDataId}/`)
    .then(response => {
      if (!response.ok) {
        // If the response status is not OK, log and return "no default chatbot"
        console.log(`No default chatbot associated with document title ID: ${selectedBusinessDataId}`);
        return null;
      }
      return response.json();
    })
    .then(data => {
      if (data) {
        console.log("data received from backend for front: ", data);
        /* Outputs: { 
             name: "test bot settings",
             age: 39,
             origin: "Shizuako",
             dream: "dreaming of marseille",
             tone: "happy",
             description: "description of bot",
             expertise: "expertise in testing",
             avatar_url: "/media/uploads/chatbotsettings/happy_bot_XIUU1l1.png"
         }*/
        document.getElementById("chatbotName").setAttribute("type", "visible");
        document.getElementById("chatbotName").innerText = `Name: ${data.name}`;
        document.getElementById("chatbotAvatar").setAttribute("style", "display: inline;");
        document.getElementById("chatbotAvatar").src = data.avatar_url;
        document.getElementById("chatbotAge").setAttribute("type", "visible");
        document.getElementById("chatbotAge").innerText = `Age: ${data.age}`;
        document.getElementById("chatbotOrigin").setAttribute("type", "visible");
        document.getElementById("chatbotOrigin").innerText = `Origin: ${data.origin}`;
        document.getElementById("chatbotDream").setAttribute("type", "visible");
        document.getElementById("chatbotDream").innerText = `Dream: ${data.dream}`;
        document.getElementById("chatbotTone").setAttribute("type", "visible");
        document.getElementById("chatbotTone").innerText = `Tone: ${data.tone}`;
        document.getElementById("chatbotDescription").setAttribute("type", "visible");
        document.getElementById("chatbotDescription").innerText = `Description: ${data.description}`;
        document.getElementById("chatbotExpertise").setAttribute("type", "visible");
        document.getElementById("chatbotExpertise").innerText = `Expertise: ${data.expertise}`;
        document.getElementById("chatbotBusinessOwner").setAttribute("type", "visible");
        document.getElementById("chatbotBusinessOwner").innerText = `Business Owner: ${data.business_owner}`;
        document.getElementById("chatbotNumber").setAttribute("type", "visible");
        document.getElementById("chatbotNumber").innerText = `Number: ${data.number}`;
      } else {

           // show the form for custom AI Personality traits
          document.getElementById("customChatbotForm").setAttribute("style", "display: inline;");

          // display default chatbot avatar could be the business logo for example
          document.getElementById("chatbotName").setAttribute("type", "hidden");
          document.getElementById("chatbotAvatar").setAttribute("style", "display: inline;");
          document.getElementById("chatbotAvatar").src = "/static/images/chatbot_dummy.png";

          // make all the other field invisible again to not see their label (Age, Dream...)
          document.getElementById("chatbotAge").setAttribute("style", "display: none;");
          document.getElementById("chatbotOrigin").setAttribute("type", "hidden");
          document.getElementById("chatbotDream").setAttribute("type", "hidden");
          document.getElementById("chatbotTone").setAttribute("type", "hidden");
          document.getElementById("chatbotDescription").setAttribute("type", "hidden");
          document.getElementById("chatbotExpertise").setAttribute("type", "hidden");
          document.getElementById("chatbotBusinessOwner").setAttribute("type", "hidden");
          document.getElementById("chatbotNumber").setAttribute("type", "hidden");
        }
    })
    .catch(error => {
      // Handle actual errors (network or unexpected issues)
      console.error('An error occurred while fetching chatbot details:', error);
    });
});

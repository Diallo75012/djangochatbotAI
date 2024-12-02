// fetching sidebar data and message send from form to send it ot django backend that will process data
document.addEventListener('DOMContentLoaded', function() {
  const messageForm = document.getElementById('message-form');
  const chatContainer = document.getElementById('chat-container');
  messageForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const messageInput = document.getElementById('message-input').value;
    console.log("MessageInput: ", messageInput);
    // straight away add the message sent by the user to the webui
    appendMessage(chatContainer, messageInput, 'user');

    // Determine if we should use default chatbot or custom fields and if they exist
    let chatbotData = {};
    const chatbotNameElem = document.getElementById('chatbotName') ? document.getElementById('chatbotName').innerText : '';
    console.log("ChatbotNameElem: ", chatbotNameElem)
    const chatbotDescriptionElem = document.getElementById('chatbotDescription') ? document.getElementById('chatbotDescription').innerText : '';
    console.log("chatbotDescriptionElem: ", chatbotDescriptionElem)
    const customchatbotNameElem = document.getElementById('customChatbotName') ? document.getElementById('customChatbotName').value : '';
    console.log("customChatbotNameElem: ", customchatbotNameElem)
    const customchatbotDescriptionElem = document.getElementById('customChatbotDescription') ? document.getElementById('customChatbotDescription').value : '';
    console.log("customchatbotDescriptionElem: ", customchatbotDescriptionElem)

    if (chatbotNameElem && chatbotDescriptionElem) {
      // Default chatbot details
      chatbotData = {
        'chatbot_name': chatbotNameElem || '',
        'chatbot_age': document.getElementById('chatbotAge') ? document.getElementById('chatbotAge').innerText : '',
        'chatbot_origin': document.getElementById('chatbotOrigin') ? document.getElementById('chatbotOrigin').innerText  : '',
        'chatbot_dream': document.getElementById('chatbotDream') ? document.getElementById('chatbotDream').innerText  : '',
        'chatbot_tone': document.getElementById('chatbotTone') ? document.getElementById('chatbotTone').innerText  : '',
        'chatbot_description': chatbotDescriptionElem || '',
        'chatbot_expertise': document.getElementById('chatbotExpertise') ? document.getElementById('chatbotExpertise').innerText  : '',
      };
      console.log("Chatbotdata default: ", chatbotData);
    } else {
      console.log("missing chatbot name or description or both");
    }

    if (customchatbotNameElem && customchatbotDescriptionElem) {
      // Custom chatbot details
      chatbotData = {
        'chatbot_name': customchatbotNameElem || '',
        'chatbot_age': document.getElementById('customChatbotAge') ? document.getElementById('customChatbotAge').value : '',
        'chatbot_origin': document.getElementById('customChatbotOrigin') ? document.getElementById('customChatbotOrigin').value : '',
        'chatbot_dream': document.getElementById('customChatbotDream') ? document.getElementById('customChatbotDream').value : '',
        'chatbot_tone': document.getElementById('customChatbotTone') ? document.getElementById('customChatbotTone').value : '',
        'chatbot_description': customchatbotDescriptionElem || '',
        'chatbot_expertise': document.getElementById('customChatbotExpertise') ? document.getElementById('customChatbotExpertise').value : '',
      };
      console.log("Chatbotdata from client sidebar form: ", chatbotData);
    } else {
      console.log("missing chatbot name or description or both");
    }

    // Prepare data for submission
    const dataToSend = {
      'message': messageInput,
      ...chatbotData
    };

    console.log("Data to send", dataToSend);
    console.log("Stringified data to send: ", JSON.stringify(dataToSend))

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
      // check what is inside data
      console.log("data from ajax call received: ", data)    

      // Append the bot response to the chat container
      appendMessage(chatContainer, data.bot_message, 'bot');

      // Scroll to the bottom after updating
      chatContainer.scrollTop = chatContainer.scrollHeight;
    })
    .catch(error => console.error(`Error: ${error}`));
  });
});


// chat side of webui appending messages to display those
/* check this function as it doesn't use the argument `container` which is the `chatContainer` sent fromt he above function*/
function appendMessage(container, message, sender) {
  console.log("Container: ", container, "Message: ", message, "Sender: ", sender)
  // creating the container space to receive messages
  const messageContainer = document.createElement('div');
  messageContainer.className = `message-container ${sender}-message`;

  // creating the avatar space <img src:"" >
  /* here we get the two urls sent by django view having the url of the chatbot/user images */
  const userAvatarUrl = document.getElementById('user-avatar').dataset.avatarUrl;
  const chatbotAvatarUrl = document.getElementById('chatbot-avatar').dataset.avatarUrl;
  const avatar = document.createElement('img');
  avatar.className = 'avatar';
  //  those two `user/chatbot_avatar` are sent in the context of the template by the django view
  avatar.src = sender === 'user' ? userAvatarUrl : chatbotAvatarUrl;
  avatar.alt = `${sender} avatar`;

  // creating the message space <div class="">InnerHTML</div>
  const messageDiv = document.createElement('div');
  messageDiv.className = 'message';
  messageDiv.innerHTML = `<p>${message}</p>`;

  // appending avatar and message to the container <div> adding <img> and <div> ></div>
  messageContainer.appendChild(avatar);
  messageContainer.appendChild(messageDiv);
  container.appendChild(messageContainer);
}

// ########### SIDEBAR CLIENT CHAT CHATBOT DETAILS DYNAMIC CHANGE WHEN USER SELECT #######

// handle dropdown document_titles in sidebar. check if there is chatbotsettings associated and display detail if yes
document.getElementById("documentTitleDropdown").addEventListener("change", function() {

  // this is to check if default chatbot setting exist to see how later in the function we display the fields with labels or not. span hidden is used in webui to catch that here
  const chatbotDefault = document.getElementById('default-chatbot').dataset.defaultChatbot;
  console.log("chatbotdefault: ", chatbotDefault);
  
  // this id from business data corresponding to the document_title row will be used to fetch from the `chat_bot` field the right chatbot data
  const selectedBusinessDataId = this.value;
  console.log("Chatbot ID: ", selectedBusinessDataId, typeof(selectedBusinessDataId));

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

        if (chatbotDefault) {
          document.getElementById("chatbotName").setAttribute("style", "display: inline;");
          document.getElementById("chatbotName").innerText = `${data.name}`;
          document.getElementById("chatbotAvatar").setAttribute("style", "display: inline;");
          document.getElementById("chatbotAvatar").src = data.avatar_url;
          document.getElementById("chatbotAge").setAttribute("style", "display: inline;");
          document.getElementById("chatbotAge").innerText = `${data.age}`;
          document.getElementById("chatbotOrigin").setAttribute("style", "display: inline;");
          document.getElementById("chatbotOrigin").innerText = `${data.origin}`;
          document.getElementById("chatbotDream").setAttribute("style", "display: inline;");
          document.getElementById("chatbotDream").innerText = `${data.dream}`;
          document.getElementById("chatbotTone").setAttribute("style", "display: inline;");
          document.getElementById("chatbotTone").innerText = `${data.tone}`;
          document.getElementById("chatbotDescription").setAttribute("style", "display: inline;");
          document.getElementById("chatbotDescription").innerText = `${data.description}`;
          document.getElementById("chatbotExpertise").setAttribute("style", "display: inline;");
          document.getElementById("chatbotExpertise").innerText = `${data.expertise}`;
          document.getElementById("chatbotBusinessOwner").setAttribute("style", "display: inline;");
          document.getElementById("chatbotBusinessOwner").innerText = `${data.business_owner}`;
          document.getElementById("chatbotNumber").setAttribute("style", "display: inline;");
          document.getElementById("chatbotNumber").innerText = `${data.number}`;
        } else {
          document.getElementById("chatbotName").setAttribute("style", "display: inline;");
          document.getElementById("chatbotName").innerText = `Name: ${data.name}`;
          document.getElementById("chatbotAvatar").setAttribute("style", "display: inline;");
          document.getElementById("chatbotAvatar").src = data.avatar_url;
          document.getElementById("chatbotAge").setAttribute("style", "display: inline;");
          document.getElementById("chatbotAge").innerText = `Age: ${data.age}`;
          document.getElementById("chatbotOrigin").setAttribute("style", "display: inline;");
          document.getElementById("chatbotOrigin").innerText = `Origin: ${data.origin}`;
          document.getElementById("chatbotDream").setAttribute("style", "display: inline;");
          document.getElementById("chatbotDream").innerText = `Dream: ${data.dream}`;
          document.getElementById("chatbotTone").setAttribute("style", "display: inline;");
          document.getElementById("chatbotTone").innerText = `Tone: ${data.tone}`;
          document.getElementById("chatbotDescription").setAttribute("style", "display: inline;");
          document.getElementById("chatbotDescription").innerText = `Description: ${data.description}`;
          document.getElementById("chatbotExpertise").setAttribute("style", "display: inline;");
          document.getElementById("chatbotExpertise").innerText = `Expertise: ${data.expertise}`;
          document.getElementById("chatbotBusinessOwner").setAttribute("style", "display: inline;");
          document.getElementById("chatbotBusinessOwner").innerText = `Business Owner: ${data.business_owner}`;
          document.getElementById("chatbotNumber").setAttribute("style", "display: inline;");
          document.getElementById("chatbotNumber").innerText = `Number: ${data.number}`;
        }
      } else {

           // show the form for custom AI Personality traits
          document.getElementById("customChatbotForm").setAttribute("style", "display: inline;");

          // display default chatbot avatar could be the business logo for example
          document.getElementById("chatbotName").setAttribute("type", "hidden");
          document.getElementById("chatbotAvatar").setAttribute("style", "display: inline;");
          document.getElementById("chatbotAvatar").src = "/static/images/chatbot_dummy.png";

          // make all the other field invisible again to not see their label (Age, Dream...)
          document.getElementById("chatbotAge").setAttribute("style", "display: none;");
          document.getElementById("chatbotOrigin").setAttribute("style", "display: none;");
          document.getElementById("chatbotDream").setAttribute("style", "display: none;");
          document.getElementById("chatbotTone").setAttribute("style", "display: none;");
          document.getElementById("chatbotDescription").setAttribute("style", "display: none;");
          document.getElementById("chatbotExpertise").setAttribute("style", "display: none;");
          document.getElementById("chatbotBusinessOwner").setAttribute("style", "display: none;");
          document.getElementById("chatbotNumber").setAttribute("style", "display: none;");
        }
    })
    .catch(error => {
      // Handle actual errors (network or unexpected issues)
      console.error('An error occurred while fetching chatbot details:', error);
    });
});

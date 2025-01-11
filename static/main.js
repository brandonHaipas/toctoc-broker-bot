function send_message(event) {
    event.preventDefault();
    input = document.getElementById("message")
    form = new FormData(event.target);
    message = form.get("message");
    console.log(message);
    new_message(message, "user");
    input.value = ""
       fetch("/message", {
          method: "POST",
          body: JSON.stringify({
            message: message,
          }),
          headers: {
            "Content-type": "application/json; charset=UTF-8"
          }
    })
  .then((response) => {
    response.json().then((data) => {
        message1 = data.message1
        new_message(message1, "bot")
        message2 = data.message2
        try {
            console.log(message2)
            if (message2 !== "") {
              list_properties(message2)  
            }
            //list_properties(message2)
        } catch(error) {
            error
        }
        
        message3 = data.message3
        console.log(message3)
        new_message(JSON.stringify(message3), "bot")
    }
                                     )
    
  })

}

function new_message(content, role) {
    new_message_element_div = document.createElement('div');
    new_message_element_div.classList.add("chat");
    chat = document.getElementById('chat');

    if (role === "bot") {
        new_message_element_div.classList.add("chat-start");
        chat_image = document.createElement('div');
        chat_image.classList.add('chat-image');
        chat_image.classList.add('avatar');
        chat_image_div = document.createElement('div');
        chat_image_div.classList.add('w-10');
        chat_image_div.classList.add('rounded-full');
        chat_img = document.createElement('img');
        chat_img.src = "https://images.scalebranding.com/angry-red-panda-logo-699ba7fb-0177-48de-8167-4a7a556fca1d.jpg";


        new_message_element_div.appendChild(chat_image);
        chat_image.appendChild(chat_image_div);
        chat_image_div.appendChild(chat_img);

    }   
    else if (role === "user") {
        new_message_element_div.classList.add("chat-end");
        
    }
            chat_bubble = document.createElement('div');
        chat_bubble.classList.add("chat-bubble");
        console.log(typeof(content))
            chat_bubble.innerHTML = content
 
            new_message_element_div.appendChild(chat_bubble);

        chat.appendChild(new_message_element_div);
}
 
function list_properties(properties) {
    new_properties_list = document.createElement('div');
    new_properties_list.classList.add('carousel')
    new_properties_list.classList.add('rounded-box')
    
    properties.forEach((prop) => {
        property_div = document.createElement('div')
        property_div.classList.add('carousel-item')
        property_div.innerHTML = "<a href='https://www.toctoc.com/propiedades/compranuevo/departamento/la-florida/edificio-refugio-new/"+prop.id+"'>"+prop.name+"</a>"
        new_properties_list.appendChild(property_div)
    })
    new_message(new_properties_list.innerHTML, "bot")
}

document.getElementById('chat-form').addEventListener('submit', send_message)
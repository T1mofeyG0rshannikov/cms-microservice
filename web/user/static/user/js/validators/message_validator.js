function validateMessage(message){
    return message.length > 0;
};


function onchangeMessage(element){
    const messageContainer = element.querySelector("#message");

    const isValid = validateUsername(messageContainer.querySelector("textarea").value);
    const errorMessage = isValid ? "" : "Напишите свое сообщение"
    setError(messageContainer, errorMessage);

    return isValid;
}

function setError(element, message){
    const errorContainer = element.querySelector(".error");

    if (errorContainer === null || errorContainer === undefined){
        const errorMessage = document.createElement("div")
        errorMessage.classList.add("error")
        errorMessage.innerHTML = message

        element.appendChild(errorMessage);
    }
    else{
        errorContainer.innerHTML = message
    }
}

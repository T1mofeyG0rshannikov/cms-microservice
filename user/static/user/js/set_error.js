function setError(containerName, message){
    const container = document.getElementById(containerName);
    const errorContainer = container.querySelector(".error");

    if (errorContainer === null || errorContainer === undefined){
        const errorMessage = document.createElement("div")
        errorMessage.classList.add("error")
        errorMessage.innerHTML = message

        container.appendChild(errorMessage);
    }

    else{
        errorContainer.innerHTML = message
    }
}

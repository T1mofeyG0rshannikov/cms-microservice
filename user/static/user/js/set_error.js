function setError(element, message){
    const errorContainer = element.querySelector(".error");

    if (errorContainer === null || errorContainer === undefined){
        const errorMessage = document.createElement("div")
        errorMessage.classList.add("error")
        errorMessage.innerHTML = message;
        if (message.length > 0){
            errorMessage.style.display = "block";
        }
        else{
            errorMessage.style.display = "none";
        }

        element.appendChild(errorMessage);
    }
    else{
        errorContainer.innerHTML = message;
        if (message.length > 0){
            errorContainer.style.display = "block";
        }
        else{
            errorContainer.style.display = "none";
        }
    }
}


function setErrors(errors, element){
    const fields = element.querySelectorAll(".field")

    for (let field of fields){
        setError(field, "")
    }

    for (let field of Object.keys(errors)) {
        setError(element.querySelector(`#${field}`), errors[field][0]);
    }
}

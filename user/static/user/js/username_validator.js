const validateUsername = (username) => {
    return username.length > 4;
};


function onchangeUsername(event){
    const usernameContainer = document.querySelector("#username");
    const isValid = validateUsername(event.target.value);
    validUsername = isValid;

    const errorContainer = usernameContainer.querySelector(".error");

    if (!isValid){
        if (errorContainer === null || errorContainer === undefined){
            const errorMessage = document.createElement("div")
            errorMessage.classList.add("error")
            errorMessage.innerHTML = "Слишком короткое имя"

            usernameContainer.appendChild(errorMessage);
        }

        else{
            errorContainer.innerHTML = "Слишком короткое имя"
        }
    }

    else{
        if (errorContainer !== null && errorContainer !== undefined){
            errorContainer.innerHTML = "";
        }
    }
}

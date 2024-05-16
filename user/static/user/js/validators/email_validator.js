const validateEmail = (email) => {
    return String(email)
        .toLowerCase()
        .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        );
};


function onchangeEmail(event){
    const isValid = validateEmail(event.target.value);
    validEmail = isValid;

    const emailContainer = document.querySelector("#email");
    const errorContainer = emailContainer.querySelector(".error");

    if (!isValid){
        if (errorContainer === null || errorContainer === undefined){
            const errorMessage = document.createElement("div")
            errorMessage.classList.add("error")
            errorMessage.innerHTML = "Введите правильный E-mail"

            emailContainer.appendChild(errorMessage);
        }

        else{
            errorContainer.innerHTML = "Введите правильный E-mail"
        }
    }

    else{
        if (errorContainer !== null && errorContainer !== undefined){
            errorContainer.innerHTML = "";
        }
    }
}

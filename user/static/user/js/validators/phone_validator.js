function onchangePhone(){
    const phoneContainer = document.querySelector("#phone");
    const errorContainer = phoneContainer.querySelector(".error");

    const isValid = phoneContainer.querySelector("input").value.length > 0;

    validPhone = isValid;

    if (!isValid){
        if (errorContainer === null || errorContainer === undefined){
            const errorMessage = document.createElement("div")
            errorMessage.classList.add("error")
            errorMessage.innerHTML = "Введите телефон"

            phoneContainer.appendChild(errorMessage);
        }

        else{
            errorContainer.innerHTML = "Введите телефон"
        }
    }

    else{
        if (errorContainer !== null && errorContainer !== undefined){
            errorContainer.innerHTML = "";
        }
    }
}

function validatePhone(phoneNumber) {
    let phoneRegex = /^\+7[0-9]{10}$/;

    if (phoneRegex.test(phoneNumber)) {
        return true;
    } else {
        return false;
    }
}

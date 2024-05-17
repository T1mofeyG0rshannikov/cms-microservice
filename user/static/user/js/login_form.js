function formValid(){
    const loginButton = document.querySelector("input[type=submit]")

    if (validPhoneOrEmail && validPassword){
        loginButton.disabled = false;
    }
    else{
        loginButton.disabled = true;
    }
}


function validatePhoneOrEmail(value){
    if (!validateEmail(value) && !validatePhone(value)){
        return false;
    }

    return true;
}


function onchangePhoneOrEmail(event){
    const isValid = validatePhoneOrEmail(event.target.value);
    validPhoneOrEmail = isValid;

    const phoneOrEmailContainer = document.querySelector("#phone_or_email");
    const errorContainer = phoneOrEmailContainer.querySelector(".error");

    if (!isValid){
        if (errorContainer === null || errorContainer === undefined){
            const errorMessage = document.createElement("div")
            errorMessage.classList.add("error")
            errorMessage.innerHTML = "Введите правильный логин"

            phoneOrEmailContainer.appendChild(errorMessage);
        }

        else{
            errorContainer.innerHTML = "Введите правильный логин"
        }
    }

    else{
        if (errorContainer !== null && errorContainer !== undefined){
            errorContainer.innerHTML = "";
        }
    }
}


function onchangePassword(event){
    const isValid = validatePassword(event.target.value);
    validPassword = isValid;

    const passwordContainer = document.querySelector("#password");
    const errorContainer = passwordContainer.querySelector(".error");

    if (!isValid){
        if (errorContainer === null || errorContainer === undefined){
            const errorMessage = document.createElement("div")
            errorMessage.classList.add("error")
            errorMessage.innerHTML = "Введите правильный пароль"

            passwordContainer.appendChild(errorMessage);
        }

        else{
            errorContainer.innerHTML = "Введите правильный пароль"
        }
    }

    else{
        if (errorContainer !== null && errorContainer !== undefined){
            errorContainer.innerHTML = "";
        }
    }
}


const phoneOrEmailInput = document.querySelector("#phone_or_email").querySelector("input")
const passwordInput = document.querySelector("#password").querySelector("input")

let validPhoneOrEmail = validatePhoneOrEmail(phoneOrEmailInput.value);
let validPassword = validatePassword(passwordInput.value);


phoneOrEmailInput.addEventListener("change", (event) => {
    onchangePhoneOrEmail(event);
    formValid();
});

passwordInput.addEventListener("change", (event) => {
    onchangePassword(event);
    formValid();
})

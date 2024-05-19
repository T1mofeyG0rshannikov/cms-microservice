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

    const errorMessage = isValid ? "" : "Введите правильный логин"
    setError("phone_or_email", errorMessage)
}


function onchangePassword(event){
    const isValid = validatePassword(event.target.value);
    validPassword = isValid;

    const errorMessage = isValid ? "" : "Введите правильный пароль"
    setError("password", errorMessage)
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

function initLoginForm(element){
    const phoneOrEmailContainer = element.querySelector("#phone_or_email");
    const passwordContainer = element.querySelector("#password");

    const phoneOrEmailInput = phoneOrEmailContainer.querySelector("input")
    const passwordInput = passwordContainer.querySelector("input")

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


    function onchangePhoneOrEmail(element){
        const isValid = validatePhoneOrEmail(phoneOrEmailInput.value);

        const errorMessage = isValid ? "" : "Введите правильный логин"
        setError(phoneOrEmailContainer, errorMessage);
        return isValid;
    }


    function onchangePassword(element){
        const isValid = validatePassword(passwordInput.value);

        const errorMessage = isValid ? "" : "слишком короткий пароль"
        setError(passwordContainer, errorMessage);
        return isValid;
    }

    let validPhoneOrEmail = validatePhoneOrEmail(phoneOrEmailInput.value);
    let validPassword = validatePassword(passwordInput.value);


    phoneOrEmailInput.addEventListener("change", (event) => {
        validPhoneOrEmail = onchangePhoneOrEmail(event);
        formValid();
    });

    passwordInput.addEventListener("change", (event) => {
        validPassword =onchangePassword(event);
        formValid();
    })
}

const loginForm = document.querySelector(".user-form")
initLoginForm(loginForm);

function sendMainToResetPassword(){
    fetch("/user/mail-to-reset-password/${user}", )
}

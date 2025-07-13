function sendMainToResetPassword(){
    fetch("/user/mail-to-reset-password/${user}", )
}

function rememberMe(){
    localStorage.setItem("bankomagRememberMe", true);
}

function rememberUserInfo(username, password){
    localStorage.setItem("bankomagUsername", username);
    localStorage.setItem("bankomagPassword", password);
}

function compliteLoginForm(){
    if (isRememberMe()){
        const form = document.getElementById("login-form");
        const loginInput = form.querySelector("#phone_or_email input");
        const passwordInput = form.querySelector("#password input");

        const login = localStorage.getItem("bankomagUsername");
        const password = localStorage.getItem("bankomagPassword");

        loginInput.value = login;
        passwordInput.value = password;
    }
}

function isAgreeToRememberMe(){
    return loginForm.querySelector(".agreed-container input").checked;
}

async function submitLoginForm(element, event, domain){
    event.preventDefault();
    const data = new FormData(element);

    const response = await loginAPI(data)

    if (response.status === 200){
        const access_token = response.data.access_token;
        const refresh_token = isAgreeToRememberMe() ? response.data.refresh_token : null;

        console.log(response)
        console.log(refresh_token)
        console.log(isAgreeToRememberMe())
        setTokens(access_token, refresh_token);

        if (isAgreeToRememberMe()){
            rememberMe();
            rememberUserInfo(data.get("phone_or_email"), data.get("password"));
        }

        window.location.replace(`${window.location.protocol}//${domain}/my`);
    }
    else if (response.status === 400){
        setErrors(response.data.errors, element)
    }
    else{
        setErrors({"password": ["Что-то пошло не так. Обновите страницу или попробуйте позже"]}, element)
    }
}

const registerFormContainer = document.querySelector(".register-form-container");
const resetPasswordFormContainer = document.querySelector(".reset-password-form-container");
const resetPasswordDialogContainer = document.querySelector(".reset-password-dialog-container");
const loginFormContainer = document.querySelector(".login-form-container");

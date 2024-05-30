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

function isRememberMe(){
    if (localStorage.getItem("bankomagRememberMe")){
        return true;
    }

    return false;
}

function compliteLoginForm(){
    if (isRememberMe()){
        const loginInput = document.querySelector("#phone_or_email input");
        const passwordInput = document.querySelector("#password input");

        const login = localStorage.getItem("bankomagUsername");
        const password = localStorage.getItem("bankomagPassword");

        loginInput.value = login;
        passwordInput.value = password;
    }
}

function isAgreeToRememberMe(){
    console.log(document.querySelector(".agreed-container input").checked);
    return document.querySelector(".agreed-container input").checked;
}

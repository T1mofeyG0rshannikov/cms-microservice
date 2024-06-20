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
    return document.querySelector(".agreed-container input").checked;
}

function submitLoginForm(element, event, domain){
    event.preventDefault();
    const data = new FormData(element);

    fetch("/user/login", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            //'X-CSRFToken': data.get("csrfmiddlewaretoken"),
        },
        body: data
    }).then(response => {
        if (response.status === 200){
            response.json().then((response) => {
                const token = response.acess_token;
                setToken(token);

                if (isAgreeToRememberMe()){
                    rememberMe();
                    rememberUserInfo(data.get("phone_or_email"), data.get("password"));
                }

                window.location.replace(`http://${domain}/user/set-token/${token}`);
            })
        }
        return response.json();
    }).then(response => {
        setErrors(response.errors, element)
    })
}

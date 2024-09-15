function validateUsername(username){
    return username.length > 0;
};


function onchangeUsername(element){
    const usernameContainer = element.querySelector("#username");

    const isValid = validateUsername(usernameContainer.querySelector("input").value);
    const errorMessage = isValid ? "" : "Укажите имя"
    setError(usernameContainer, errorMessage);

    return isValid;
}

function onchangePhoneOrEmail(element){
    const phoneOrEmailContainer = element.querySelector("#phone_or_email");

    const isValid = phoneOrEmailContainer.querySelector("input").value.length > 0;

    const errorMessage = isValid ? "" : "Введите почту или телеофон"
    setError(phoneOrEmailContainer, errorMessage);

    return isValid;
}

function onchangePassword(element){
    const passwordContainer = element.querySelector("#password");

    const isValid = passwordContainer.querySelector("input").value.length > 0;

    const errorMessage = isValid ? "" : "Введите пароль"
    setError(passwordContainer, errorMessage);

    return isValid;
}

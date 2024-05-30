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

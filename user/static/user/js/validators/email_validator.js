const validateEmail = (email) => {
    return String(email)
        .toLowerCase()
        .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    ) !== null;
};


function onchangeEmail(element){
    const emailContainer = element.querySelector("#email");

    const isValid = validateEmail(emailContainer.querySelector("input").value);

    const errorMessage = isValid ? "" : "Введите корректный email"
    setError(emailContainer, errorMessage);

    return isValid;
}

const validateEmail = (email) => {
    return String(email)
        .toLowerCase()
        .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        );
};


function onchangeEmail(event){
    const isValid = validateEmail(event.target.value);
    validEmail = isValid;

    const errorMessage = isValid ? "" : "Введите правильный E-mail"
    setError("email", errorMessage)
}

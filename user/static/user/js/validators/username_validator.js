const validateUsername = (username) => {
    return username.length > 0;
};


function onchangeUsername(event){
    const isValid = validateUsername(event.target.value);
    validUsername = isValid;

    const errorMessage = isValid ? "" : "Слишком короткое имя"

    setError("username", errorMessage)
}

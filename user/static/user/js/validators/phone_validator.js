function onchangePhone(element){
    const phoneContainer = element.querySelector("#phone");
    //const isValid = validatePhone(phoneContainer.querySelector("input").value);
    const isValid = phoneContainer.querySelector("input").value.length > 0;

    const errorMessage = isValid ? "" : "Введите правильный телефон"
    setError(phoneContainer, errorMessage);
    return isValid;
}

function validatePhone(phoneNumber) {
    let phoneRegex = /^\+7[0-9]{10}$/;

    if (phoneRegex.test(phoneNumber)) {
        return true;
    } else {
        return false;
    }
}

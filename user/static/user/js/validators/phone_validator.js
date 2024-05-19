function onchangePhone(){
    const phoneContainer = document.querySelector("#phone");

    const isValid = phoneContainer.querySelector("input").value.length > 0;

    validPhone = isValid;

    const errorMessage = isValid ? "" : "Введите телефон"

    setError("phone", errorMessage)
}

function validatePhone(phoneNumber) {
    let phoneRegex = /^\+7[0-9]{10}$/;

    if (phoneRegex.test(phoneNumber)) {
        return true;
    } else {
        return false;
    }
}

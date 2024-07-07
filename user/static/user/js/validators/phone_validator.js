function onchangePhone(element){
    const phoneContainer = element.querySelector("#phone");

    let phone = phoneContainer.querySelector("input").value;

    const numberPattern = /\d+/g;
    phone = phone.match( numberPattern ).join('');

    const isValid = phone.length > 10;

    const errorMessage = isValid ? "" : "Введите корректный телефон"
    setError(phoneContainer, errorMessage);
    return isValid;
}

function validatePhone(phoneNumber) {
    const numberPattern = /\d+/g;
    phoneNumber = phoneNumber.match( numberPattern );

    if (phoneNumber !== null){
        phoneNumber = phoneNumber.join('');

        if (phoneNumber[0] !== '+'){
            phoneNumber = '+' + phoneNumber;
        }
    }

    console.log(phoneNumber);

    let phoneRegex = /^\+7[0-9]{10}$/;

    if (phoneRegex.test(phoneNumber)) {
        return true;
    } else {
        return false;
    }
}

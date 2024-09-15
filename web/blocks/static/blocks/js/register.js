function initForm(element){
    function formValid(){
        const registerButton = element.querySelector("input[type=submit]")

        if (validEmail && validPhone && validUsername){
            registerButton.disabled = false;
        }
        else{
            registerButton.disabled = true;
        }
    }

    const emailInput = element.querySelector("#email").querySelector("input");
    const usernameInput = element.querySelector("#username").querySelector("input");
    const phoneInput = element.querySelector("#phone").querySelector("input");

    let validEmail = validateEmail(emailInput.value);
    let validUsername = validateUsername(usernameInput.value);
    let validPhone = validatePhone(phoneInput.value);

    emailInput.addEventListener("input", () => {
        validEmail = validateEmail(element.querySelector("#email input").value);
        formValid();
    });

    emailInput.addEventListener("change", () => {
        const emailContainer = element.querySelector("#email");

        const errorMessage = validEmail ? "" : "Введите корректный email"
        setError(emailContainer, errorMessage);
    })

    usernameInput.addEventListener("input", () => {
        validUsername = validateUsername(element.querySelector("#username input").value);
        formValid();
    });

    usernameInput.addEventListener("change", () => {
        const usernameContainer = element.querySelector("#username");

        const errorMessage = validUsername ? "" : "Укажите имя"
        setError(usernameContainer, errorMessage);
    })

    $("input[name=phone]").mask("+7 (999) 999-99-99")
    $("input[name=phone]").on("keyup", () => {
        validPhone = validatePhone(element.querySelector("#phone input").value);
        formValid();
    })

    $("input[name=phone]").on("change", () => {
        validPhone = validatePhone(element.querySelector("#phone input").value);
        const phoneContainer = element.querySelector("#phone");

        const errorMessage = validPhone ? "" : "Введите корректный телефон"
        setError(phoneContainer, errorMessage);
        formValid();
    })
}

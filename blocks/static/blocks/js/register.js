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

    emailInput.addEventListener("change", () => {
        validEmail = onchangeEmail(element);
        validPhone = onchangePhone(element);
        validUsername = onchangeUsername(element);
        formValid()
    });

    usernameInput.addEventListener("change", () => {
        validEmail = onchangeEmail(element);
        validPhone = onchangePhone(element);
        validUsername = onchangeUsername(element);
        formValid()
    })

    $("input[name=phone]").mask("+7 (999) 999-99-99")
    $("input[name=phone]").on("change", () => {
        validEmail = onchangeEmail(element);
        validPhone = onchangePhone(element);
        validUsername = onchangeUsername(element);
        formValid();
    })
}

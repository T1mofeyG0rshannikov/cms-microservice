const registerForm = document.getElementById("register-form");


function initRegisterForm(){
    function formValid(){
        const registerButton = registerForm.querySelector("input[type=submit]")
        const agreed = checkbox.checked;

        if (validEmail && validPhone && validUsername && agreed){
            registerButton.disabled = false;
        }
        else{
            registerButton.disabled = true;
        }
    }

    const emailInput = registerForm.querySelector("#email").querySelector("input");
    const usernameInput = registerForm.querySelector("#username").querySelector("input");
    const phoneInput = registerForm.querySelector("#phone").querySelector("input");
    const checkbox = registerForm.querySelector(".agreed-container").querySelector("input[type=checkbox]")


    let validEmail = validateEmail(emailInput.value);
    let validUsername = validateUsername(usernameInput.value);
    let validPhone = validatePhone(phoneInput.value);


    checkbox.addEventListener("change", formValid)

    emailInput.addEventListener("change", () => {
        validEmail = onchangeEmail(registerForm);
        formValid()
    });

    usernameInput.addEventListener("change", () => {
        validUsername = onchangeUsername(registerForm);
        formValid()
    })

    phoneInput.addEventListener("change", () => {
        validPhone = onchangePhone(registerForm);
        formValid()
    })

    $("input[name=phone]").mask("+7 (999) 999-99-99")
    $("input[name=phone]").on("change", () => {
        validPhone = onchangePhone(registerForm);
        formValid()
    })
}

initRegisterForm()

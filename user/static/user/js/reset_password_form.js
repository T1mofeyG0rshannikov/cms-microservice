function initResetPasswordForm(element){
    function formValid(){
        const registerButton = element.querySelector("input[type=submit]")

        if (validEmail){
            registerButton.disabled = false;
        }
        else{
            registerButton.disabled = true;
        }
    }

    const emailInput = element.querySelector("#email").querySelector("input");

    let validEmail = validateEmail(emailInput.value);


    emailInput.addEventListener("change", () => {
        validEmail = onchangeEmail(element);
        formValid()
    });
}

const form = document.querySelector(".user-form")
initResetPasswordForm(form);

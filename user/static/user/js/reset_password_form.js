function formValid(){
    const registerButton = document.querySelector("input[type=submit]")

    if (validEmail){
        registerButton.disabled = false;
    }
    else{
        registerButton.disabled = true;
    }
}

const emailInput = document.querySelector("#email").querySelector("input");

let validEmail = validateEmail(emailInput.value);


emailInput.addEventListener("change", event => {
    onchangeEmail(event);
    formValid()
});

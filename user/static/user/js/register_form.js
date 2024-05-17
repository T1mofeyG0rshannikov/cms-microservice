function formValid(){
    const registerButton = document.querySelector("input[type=submit]")

    if (validEmail && validPhone && validUsername){
        registerButton.disabled = false;
    }
    else{
        registerButton.disabled = true;
    }
}

const emailInput = document.querySelector("#email").querySelector("input");
const usernameInput = document.querySelector("#username").querySelector("input");
const phoneInput = $("input[name=phone]");


let validEmail = validateEmail(emailInput.value);
let validUsername = validateUsername(usernameInput.value);
let validPhone = validatePhone(phoneInput.value);


emailInput.addEventListener("change", event => {
    onchangeEmail(event);
    formValid()
});

usernameInput.addEventListener("change", event => {
    onchangeUsername(event);
    formValid()
})

phoneInput.mask("+7 (999) 999-99-99");
phoneInput.on("change", () => {
    onchangePhone();
    formValid()
})

function formValid(){
    const registerButton = document.querySelector("input[type=submit]")
    const agreed = checkbox.checked;
    console.log(agreed)

    if (validEmail && validPhone && validUsername && agreed){
        registerButton.disabled = false;
    }
    else{
        registerButton.disabled = true;
    }
}

const emailInput = document.querySelector("#email").querySelector("input");
const usernameInput = document.querySelector("#username").querySelector("input");
const phoneInput = $("input[name=phone]");
const checkbox = document.querySelector(".agreed-container").querySelector("input[type=checkbox]")


let validEmail = validateEmail(emailInput.value);
let validUsername = validateUsername(usernameInput.value);
let validPhone = validatePhone(phoneInput.value);


checkbox.addEventListener("change", event => {
    formValid()
})

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

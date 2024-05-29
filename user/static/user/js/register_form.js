function formValid(){
    const registerButton = document.querySelector("input[type=submit]")
    const agreed = checkbox.checked;

    if (validEmail && validPhone && validUsername && agreed){
        registerButton.disabled = false;
    }
    else{
        registerButton.disabled = true;
    }
}

const emailInput = document.querySelector("#email").querySelector("input");
const usernameInput = document.querySelector("#username").querySelector("input");
const phoneInput = document.querySelector("#phone").querySelector("input");
const checkbox = document.querySelector(".agreed-container").querySelector("input[type=checkbox]")


let validEmail = validateEmail(emailInput.value);
let validUsername = validateUsername(usernameInput.value);
let validPhone = validatePhone(phoneInput.value);


checkbox.addEventListener("change", event => {
    formValid()
})

emailInput.addEventListener("change", () => {
    validEmail = onchangeEmail(document);
    formValid()
});

usernameInput.addEventListener("change", () => {
    validUsername = onchangeUsername(document);
    formValid()
})

phoneInput.addEventListener("change", () => {
    validPhone = onchangePhone(document);
    formValid()
})

$("input[name=phone]").mask("+7 (999) 999-99-99")
$("input[name=phone]").on("change", () => {
    validPhone = onchangePhone(document);
    formValid()
})

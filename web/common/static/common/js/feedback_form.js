const feedbackForm = document.getElementById("feedback-form");
const feedbackFormContainer = document.querySelector(".feedback-form-container");


function initFeedbackForm(){
    function formValid(){
        const sendButton = feedbackForm.querySelector("input[type=submit]")

        if (validEmail && validPhone && validUsername){
            sendButton.disabled = false;
        }
        else{
            sendButton.disabled = true;
        }
    }

    const emailInput = feedbackForm.querySelector("#email").querySelector("input");
    const usernameInput = feedbackForm.querySelector("#username").querySelector("input");
    const phoneInput = feedbackForm.querySelector("#phone").querySelector("input");


    let validEmail = validateEmail(emailInput.value);
    let validUsername = validateUsername(usernameInput.value);
    let validPhone = validatePhone(phoneInput.value);


    emailInput.addEventListener("change", () => {
        validEmail = onchangeEmail(feedbackForm);
        formValid()
    });

    usernameInput.addEventListener("change", () => {
        validUsername = onchangeUsername(feedbackForm);
        formValid()
    })

    phoneInput.addEventListener("change", () => {
        validPhone = onchangePhone(feedbackForm);
        formValid()
    })

    $("input[name=phone]").mask("+7 (999) 999-99-99")
    $("input[name=phone]").on("change", () => {
        validPhone = onchangePhone(feedbackForm);
        formValid()
    })
}

initFeedbackForm()

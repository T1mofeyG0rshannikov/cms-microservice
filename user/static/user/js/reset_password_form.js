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

    emailInput.addEventListener("change", () => {
        validEmail = onchangeEmail(element);
        formValid();
    });
}

const form = document.querySelector(".reset-password-form")
initResetPasswordForm(form);


function submitResetPasswordForm(element, event){
    event.preventDefault();

    const data = new FormData(element);

    fetch("/user/reset-password", {
        method: "POST",
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            //'X-CSRFToken': data.get("csrfmiddlewaretoken"),
        },
        body: data
    }).then(response => {
        if (response.status === 200){
           document.querySelector(".message").innerHTML = "Вам на почту пришло письмо с ссылкой для сброса пароля";
        }
        return response.json();
    }).then(response => {
        setErrors(response.errors, element)
    })
}

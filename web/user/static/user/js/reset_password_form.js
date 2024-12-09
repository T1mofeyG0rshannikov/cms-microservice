function initResetPasswordForm(element){
    const emailInput = element.querySelector("#email").querySelector("input");

    emailInput.addEventListener("change", () => {
        validEmail = onchangeEmail(element);
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
            'X-CSRFToken': data.get("csrfmiddlewaretoken")
        },
        body: data
    }).then(response => {
        if (response.status === 200){
            openFormPopup(resetPasswordDialogContainer);
           /*document.querySelector(".message").innerHTML = "Вам на почту пришло письмо с ссылкой для сброса пароля";*/
        }
        return response.json();
    }).then(response => {
        setErrors(response.errors, element)
    })
}

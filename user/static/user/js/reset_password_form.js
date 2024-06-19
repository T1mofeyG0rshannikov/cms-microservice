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


function submitResetPasswordFormForm(element, event){
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
            response.json().then((response) => {
                document.querySelector(".message").innerHTML = response.message;
            })
        }
        return response.json();
    }).then(response => {
        setErrors(response.errors, element)
    })
}

const changePasswordForm = document.querySelector(".change-password-form");

function onSubmitChangePasswordForm(domain, element, event){
    event.preventDefault();

    const data = new FormData(element);
    const token = getToken();

    fetch(`/my/change-password`, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': `${token}`,
        },
        body: data
    }).then(response => {
        if (response.status === 200){
            setErrors({}, element)
            console.log("success");
            const access_token = response.json().access_token;
            setToken(access_token);
            closeForm(changePasswordForm);

            window.location.replace(`${window.location.protocol}//${domain}/user/set-token/${token}`);
            return;
        }
        return response.json();
    }).then(response => {
        setErrors({}, element)
        setErrors(response.errors, element)
    })
}


const form = document.querySelector(".change-password-form");
const button = form.querySelector("button");


const currentpasswordContainer = form.querySelector("#current_password")
const passwordContainer = form.querySelector("#password")
const repeatPasswordContainer = form.querySelector("#repeat_password")

const input0 = currentpasswordContainer.querySelector("input");
const input1 = passwordContainer.querySelector("input");
const input2 = repeatPasswordContainer.querySelector("input");

let touchedPassword2 = false;


input0.addEventListener("input", validateForm)
input0.addEventListener("change", () => {
    const password0 = input0.value;

    if (password0.length === 0){
        setError(currentpasswordContainer, "Введите текущий пароль");
        return;
    }
})

input1.addEventListener("input", validateForm)
input1.addEventListener("change", () => {
    const password1 = input1.value;
    const password2 = input2.value;

    if (containsCyrillic(password1)){
        setError(passwordContainer, "Только латинские буквы, цифры и символы");
        return;
    }

    if (password1.length < 6){
        setError(passwordContainer, "Длина пароля не менее 6 символов")
        button.disabled = true;
        return;
    }

    if (password1 !== password2 && password2.length > 0){
        setError(repeatPasswordContainer, "Пароли не совпадают");
        return;
    }
})

input2.addEventListener("input", () => {
    touchedPassword2 = true;
    validateForm();
})

input2.addEventListener("change", () => {
    touchedPassword2 = true;
    const password1 = input1.value;
    const password2 = input2.value;

    if (password1 !== password2 && password2.length > 0){
        setError(repeatPasswordContainer, "Пароли не совпадают");
        return;
    }
})

function validateForm(){
    const button = form.querySelector("button");

    const password0 = input0.value;
    const password1 = input1.value;
    const password2 = input2.value;

    setError(passwordContainer, "");
    setError(repeatPasswordContainer, "");

    if (containsCyrillic(password1)){
        return;
    }

    if (password1.length < 6){
        button.disabled = true;
        return;
    }

    if (password1 !== password2 || password0.length === 0){
        const button = form.querySelector("button");
        button.disabled = true;
        return;
    }

    button.disabled = false;
}

function openChangePasswordForm(){
    openForm(changePasswordForm);
    fetch("/site_statistics/opened-change-password-form")
}

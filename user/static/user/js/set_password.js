function initSetPasswordForm(){
    const form = document.querySelector(".user-form");

    const passwordContainer = form.querySelector("#password")
    const repeatPasswordContainer = form.querySelector("#repeat_password")

    const input1 = passwordContainer.querySelector("input")
    input1.addEventListener("change", validateForm)

    const input2 = repeatPasswordContainer.querySelector("input")
    input2.addEventListener("input", () => {
        validateForm();
        edited = true;
    })

    input2.addEventListener("change", () => {
        const password1 = input1.value;
        const password2 = input2.value;

        if (password1 !== password2){
            setError(repeatPasswordContainer, "Пароли не совпадают")
            button.disabled = true;
            return;
        }
    })

    function validateForm(){
        const button = form.querySelector("input[type=submit]");

        const password1 = input1.value;
        const password2 = input2.value;

        if (password1.length < 6){
            setError(passwordContainer, "Длина пароля не менее 6 символов")
            button.disabled = true;
            return;
        }

        if (containsCyrillic(password1)){
            setError(repeatPasswordContainer, "Только латинские буквы, цифры и символы")
            button.disabled = true;
            return;
        }

        if (password1 !== password2){
            button.disabled = true;
            return;
        }

        setError(passwordContainer, "")
        setError(repeatPasswordContainer, "")
        button.disabled = false;
    }

    edited = false;
}

initSetPasswordForm();

function initSetPasswordForm(){
    const form = document.querySelector("form.set-password-form");

    const passwordContainer = form.querySelector("#password")
    const repeatPasswordContainer = form.querySelector("#repeat_password")

    const input1 = passwordContainer.querySelector("input");
    const input2 = repeatPasswordContainer.querySelector("input");
    
    input1.addEventListener("input", validateForm)
    input1.addEventListener("change", () => {
        const password1 = input1.value;
        const password2 = input2.value;

        if (password1 !== password2){
            setError(passwordContainer, "Пароли не совпадают");
            const button = form.querySelector("input[type=submit]");
            button.disabled = true;
            return;
        }
    })

    input2.addEventListener("input", () => {
        validateForm();
        edited = true;
    })

    input2.addEventListener("change", () => {
        const password1 = input1.value;
        const password2 = input2.value;

        if (password1 !== password2){
            setError(repeatPasswordContainer, "Пароли не совпадают");
            const button = form.querySelector("input[type=submit]");
            button.disabled = true;
            return;
        }
    })

    function validateForm(){
        const button = form.querySelector("input[type=submit]");

        const password1 = input1.value;
        const password2 = input2.value;

        setError(passwordContainer, "");
        setError(repeatPasswordContainer, "");

        if (password1.length < 6){
            setError(passwordContainer, "Длина пароля не менее 6 символов")
            button.disabled = true;
            return;
        }

        if (containsCyrillic(password1)){
            setError(passwordContainer, "Только латинские буквы, цифры и символы")
            button.disabled = true;
            return;
        }

        if (password1 !== password2){
            button.disabled = true;
            return;
        }

        button.disabled = false;
    }

    edited = false;
}

initSetPasswordForm();


function submitSetPasswordForm(element, event, domain, token){
    event.preventDefault();
    const data = new FormData(element);

    fetch(`http://${domain}/user/password/${token}`, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: data
    }).then(response => {
        if (response.status === 200){
            response.json().then((response) => {
                const token = response.access_token;
                setToken(token);
                window.location.replace(`http://${domain}/user/set-token/${token}`);
            })
        }
        return response.json();
    }).then(response => {
        setErrors(response.errors, element)
    })
}

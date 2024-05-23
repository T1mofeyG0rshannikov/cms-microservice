function validateForm(){
    const errorContainer = document.querySelector("#password").querySelector(".error");
    const button = document.querySelector("input[type=submit]");

    const password1 = document.querySelector("input[name=password]").value;
    const password2 = document.querySelector("input[name=repeat_password]").value;

    if (password1.length < 6){
        setError("password", "Длина пароля не менее 6 символов")
        button.disabled = true;
        return;
    }

    if (containsCyrillic(password1)){
        setError("password", "Только латинские буквы, цифры и символы")
        button.disabled = true;
        return;
    }

    if (password1 !== password2){
        setError("password", "Пароли не совпадают")
        button.disabled = true;
        return;
    }

    errorContainer.innerHTML = "";
    button.disabled = false;
}

edited = false;

const input1 = document.querySelector("input[name=password]")
input1.addEventListener("change", validateForm)

const input2 = document.querySelector("input[name=repeat_password]")
input2.addEventListener("change", () => {
    validateForm();
    edited = true;
})

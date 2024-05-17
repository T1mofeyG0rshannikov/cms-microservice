function validateForm(){
    const errorContainer = document.querySelector("#password").querySelector(".error");
    const button = document.querySelector("input[type=submit]");

    const password1 = document.querySelector("input[name=password]").value;
    const password2 = document.querySelector("input[name=repeat_password]").value;

    if (password1.length < 6){
        errorContainer.innerHTML = "Слишком короткий пароль"
        button.disabled = true;
        return
    }

    if (password1 !== password2 && edited){
        errorContainer.innerHTML = "Пароли не совпадают"
        button.disabled = true;
        return
    }

    errorContainer.innerHTML = "";
    button.disabled = false;
}

edited = false;

const input1 = document.querySelector("input[name=password]")
input1.addEventListener("change", () => validateForm())

const input2 = document.querySelector("input[name=repeat_password]")
input2.addEventListener("change", () => validateForm())
input2.addEventListener("change", () => edited = true)

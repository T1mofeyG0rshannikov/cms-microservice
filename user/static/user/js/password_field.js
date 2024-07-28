document.addEventListener("DOMContentLoaded", () => {
    const passwordContainers = document.querySelectorAll(".password")

    for (let passwordContainer of passwordContainers){
        const eye = passwordContainer.querySelector(".eye");
        const passwordInput = passwordContainer.querySelector("input");

        eye.addEventListener("click", () => {
            if (passwordInput.type == "password"){
                passwordInput.type = "text";
                eye.src = "/static/user/images/eye.png";
            }
            else{
                passwordInput.type = "password";
                eye.src = "/static/user/images/eye-cross.png";
            }
        })
    }
    }
);

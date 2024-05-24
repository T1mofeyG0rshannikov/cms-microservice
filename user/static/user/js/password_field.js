const passwordContainer = document.querySelector("#password")

const eye = passwordContainer.querySelector(".eye");
const passwordInput = passwordContainer.querySelector("input");

console.log(eye)
console.log(passwordInput)

eye.addEventListener("click", (event) => {
    console.log(passwordInput.type)
    if (passwordInput.type == "password"){
        passwordInput.type = "text";
        eye.src = "/static/user/images/eye.png";
    }
    else{
        passwordInput.type = "password";
        eye.src = "/static/user/images/eye-cross.png";
    }
})



const repeatPasswordContainer = document.querySelector("#repeat_password")

const repeatPasswordEye = repeatPasswordContainer.querySelector(".eye");
const repeatPasswordInput = repeatPasswordContainer.querySelector("input");

repeatPasswordEye.addEventListener("click", (event) => {
    if (repeatPasswordInput.type == "password"){
        repeatPasswordInput.type = "text";
        repeatPasswordEye.src = "/static/user/images/eye.png";
    }
    else{
        repeatPasswordInput.type = "password";
        repeatPasswordEye.src = "/static/user/images/eye-cross.png";
    }
})

function openAsideMenu(){
    const menu = document.getElementById("aside-menu");
    menu.style.display = "flex";
    document.body.style.overflow = "hidden";

    const burger = document.querySelector(".burger")
    burger.innerHTML = `<img src="static/blocks/images/cross.png" />`;
    burger.removeEventListener("click", openAsideMenu)
    burger.addEventListener("click", closeAsideMenu)
}

function closeAsideMenu(){
    const menu = document.getElementById("aside-menu");
    menu.style.display = "none";
    document.body.style.overflow = "auto";

    const burger = document.querySelector(".burger")
    burger.innerHTML = `<img src="static/blocks/images/menu.png" />`;
    burger.removeEventListener("click", closeAsideMenu)
    burger.addEventListener("click", openAsideMenu)
}


const burger = document.querySelector(".burger")
burger.addEventListener("click", openAsideMenu);

const loginForm = document.getElementById("login-form");
const loginFormContainer = document.querySelector(".login-form-container")

function openLoginForm(){
    loginFormContainer.style.display = "flex";
}

function closeLoginForm(){
    loginFormContainer.style.display = "none";
}

loginFormContainer.addEventListener("mousedown", event => {
    if (!loginForm.contains(event.target)){
        closeLoginForm();
    }
})

const loginButtons = document.querySelectorAll("#login-button")
console.log(loginButtons);

for (let loginButton of loginButtons){
    loginButton.addEventListener("click", () => {
        console.log("open");
        openLoginForm()
    });
}

function openAsideMenu(){
    const menu = document.getElementById("aside-menu");
    menu.style.display = "flex";
    document.body.style.overflow = "hidden";

    const burger = document.querySelector(".burger")
    burger.innerHTML = `<img src="static/common/images/cross.png" />`;
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

function openLoginForm(domain){
    const token = getToken();

    fetch(`${window.location.protocol}//${domain}/user/get-user-info`, {
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': `${token}`
        }
    }).then(response => {
        if (response.status === 200){
            window.location.replace(`${window.location.protocol}//${domain}/my/`)
        }
        else if (response.status === 401){
            compliteLoginForm();
            loginFormContainer.style.animation = "showPopup .3s";
            loginFormContainer.style.display = "flex";
        }
        return response.status;
    })
}

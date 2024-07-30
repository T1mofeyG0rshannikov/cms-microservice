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
    console.log(domain, "domain")
    console.log(`http://${domain}/user/get-user-info`, "path")

    fetch(`http://${domain}/user/get-user-info`, {
        method: "get",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': `${token}`
        }
    }).then(response => {
        if (response.status === 200){
            response.json().then(() => {
                window.location.replace(`http://${domain}/my/`)
            })
        }
        return response.status;
    }).then(status => {
        if (status === 401){
            compliteLoginForm();
            loginFormContainer.style.animation = "showPopup .3s";
            loginFormContainer.style.display = "flex";
        }
    })
}

document.querySelectorAll(".form-container").forEach(form => {
    form.addEventListener("mousedown", event => {
        if (!form.querySelector("form").contains(event.target)){
            closeFormPopup(form);
        }
    })
})

$(document).keyup(function(e) {
    if (e.key === "Escape"){
        const popups = document.querySelectorAll(".form-container")
        for (let popup of popups){
            closeFormPopup(popup);
        }
   }
});
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

async function openLoginForm(domain){
    const response = await getUserAPI(domain)
    console.log(response)
    if (response.status === 200){
        const accessToken = getToken()
        const refreshToken = getRefreshToken()
        window.location.replace(`${window.location.protocol}//${domain}/user/set-token/${accessToken}/${refreshToken}`);
    }
    else if (response.status === 401){
        if (isRememberMe()){
            const r = await refreshTokensAPI()
            if (r.status === 200){
                const accessToken  = r.data.access_token
                const refreshToken = r.data.refresh_token
                window.location.replace(`${window.location.protocol}//${domain}/user/set-token/${accessToken}/${refreshToken}`);
            } else{
                compliteLoginForm();
                loginFormContainer.style.animation = "showPopup .3s";
                loginFormContainer.style.display = "flex";
            }
        } else{
            compliteLoginForm();
            loginFormContainer.style.animation = "showPopup .3s";
            loginFormContainer.style.display = "flex";
        }
    }
}

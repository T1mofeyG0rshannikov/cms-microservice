function logout(){
    deleteToken();
    window.location.replace("/user/logout");
    fetch("/user/logout")
}

const logoutElem = document.querySelector("header .inner .logout");
logoutElem.addEventListener("click", logout);

fetch("/user/get-user-info", {
    method: "get",
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': `${getToken()}`
    }
}).then(response => response.json()).
then(user => {
    console.log(user);
    document.querySelector("#username").innerHTML = user.username
})

function logout(){
    deleteToken();
    window.location.replace("/user/logout");
    fetch("/user/logout")
}

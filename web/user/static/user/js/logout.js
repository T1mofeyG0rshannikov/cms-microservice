function logout(){
    deleteTokens();
    window.location.replace("/user/logout");
    fetch("/user/logout")
}

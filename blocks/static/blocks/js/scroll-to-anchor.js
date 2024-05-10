function smoothScroll(blockID){
    closeAsideMenu()
    document.body.style.overflow = "auto";
    document.getElementById(blockID.substr(1)).scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    })
}

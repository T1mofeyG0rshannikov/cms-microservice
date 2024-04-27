function smoothScroll(blockID){
    document.getElementById(blockID.substr(1)).scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    })
}

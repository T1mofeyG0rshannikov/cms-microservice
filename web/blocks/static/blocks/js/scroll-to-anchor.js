function smoothScroll(blockID){
    closeAsideMenu();

    if (blockID[0] != "#"){
        window.location.href = blockID;
        blockID = "#" + blockID;
    }

    document.body.style.overflow = "auto";
    document.getElementById(blockID.substr(1)).scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    })
}

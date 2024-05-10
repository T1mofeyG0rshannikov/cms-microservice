function openAsideMenu(){
    const menu = document.getElementById("aside-menu");
    //menu.style.width = "300px";
    //menu.style.right = "0px";
    menu.style.display = "flex";
    document.body.style.overflow = "hidden";

    const burger = document.querySelector(".burger")
    burger.innerHTML = `<img src="static/blocks/images/cross.png" />`;
    burger.removeEventListener("click", openAsideMenu)
    burger.addEventListener("click", closeAsideMenu)
}

function closeAsideMenu(){
    const menu = document.getElementById("aside-menu");
   // menu.style.width = "0px";
    //menu.style.right = "-300px";
    menu.style.display = "none";
    document.body.style.overflow = "auto";

    const burger = document.querySelector(".burger")
    burger.innerHTML = `<img src="static/blocks/images/menu.png" />`;
    burger.removeEventListener("click", closeAsideMenu)
    burger.addEventListener("click", openAsideMenu)
}


const burger = document.querySelector(".burger")
burger.addEventListener("click", openAsideMenu)

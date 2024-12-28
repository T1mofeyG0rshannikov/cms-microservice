const content = document.querySelector("#content");
const nav = document.querySelector("header");
const menu = document.querySelector(".menu");


content.style.minHeight = `calc(100% - ${nav.getBoundingClientRect().height}px)`;
menu.style.maxHeight = `calc(100vh - ${nav.getBoundingClientRect().height}px)`


const menuUrls = [
    "/my/",
    "/my/site",
    "/my/products",
    "/my/links",
    "/my/refs",
    "/my/ads",
    "/my/materials",
    "/my/stat",
    "/my/manuals",
    "/my/si",
    "/my/messanger"
]

function activeMenuItem(url){
    document.querySelectorAll(".menu li").forEach(li => {
        li.classList.remove("active")
    })

    if (menuUrls.indexOf(url) > -1){
        document.querySelectorAll(".menu li")[menuUrls.indexOf(url)].classList.add("active");
    }
}

function loadProfileContent(templateName, url){
    history.pushState(null, '', url);
    activeMenuItem(url)

    fetch(`/get-template-${templateName}?url=${url}`).then(response => response.json()).then(response => {
        const template = response.content;
        const content = document.querySelector(".account-main");
        content.innerHTML = template;
        document.title = response.title;

        if (templateName === "refs"){
            initRefsContent();
        }

        else if (templateName === "products"){
            initUserProducts();
        }

        else if (templateName === "ideas"){
            initIdeas();
        }
    })
}

document.querySelector("main").style.maxHeight = `calc(100vh - ${nav.getBoundingClientRect().height}px)`;

const content = document.querySelector("#content");
const nav = document.querySelector("header");

content.style.minHeight = `calc(100% - ${nav.getBoundingClientRect().height}px)`;

const menuUrls = [
    "/my/",
    "/my/site",
    "/my/links",
    "/my/refs",
    "/my/ads",
    "/my/materials",
    "/my/stat",
    "/my/te",
    "/my/si"
]

function activeMenuItem(url){
    document.querySelectorAll(".menu li").forEach(li => {
        li.classList.remove("active")
    })

    document.querySelectorAll(".menu li")[menuUrls.indexOf(url)].classList.add("active")
}

function loadProfileContent(templateName, url){
    history.pushState(null, '', url);
    activeMenuItem(url)

    fetch(`/get-template-${templateName}`).then(response => response.json()).then(response => {
        const template = response.content;
        const content = document.querySelector(".account-main");
        content.innerHTML = template;
        document.title = response.title;

        if (templateName === "refs-content"){
            initRefsContent();
        }
    })
}

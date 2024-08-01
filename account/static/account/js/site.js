function stopSite(element){
    const token = getToken();

    fetch(`/domain/stop`, {
        method: "get",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': `${token}`
        }
    }).then(respose => {
        if (respose.status === 200){
            console.log("success");
            element.innerHTML = "возобновить"
            $(element).attr("onclick", "activateSite(this)");
        }
    })
}

function activateSite(element){
    const token = getToken();

    fetch(`/domain/activate`, {
        method: "get",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': `${token}`
        }
    }).then(respose => {
        if (respose.status === 200){
            element.innerHTML = "остановить"
            $(element).attr("onclick", "stopSite(this)");
        }
    })
}

let siteForm = document.querySelector(".site-form");

function openSiteForm(){
    siteForm = document.querySelector(".site-form");
    const logo = siteForm.querySelector("#logo img");
    logo.src = $(logo).attr("default");
    siteForm.querySelector("#file").value = "";

    openForm(siteForm);
}

const openSiteFormButton = document.querySelector("#open-site-form");
openSiteFormButton.addEventListener("click", () => openSiteForm());

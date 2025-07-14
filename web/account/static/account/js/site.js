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
let socialsForm = document.querySelector(".socials-form");

function setSiteFormValues(site){
    siteForm.querySelector("input[name=subdomain]").value = site.subdomain ? site.subdomain : ''
    siteForm.querySelector("input[name=name]").value = site.name ? site.name : ''
    
    siteForm.querySelectorAll("#font_id option").forEach(o => {
        if (o.textContent === site.font){
            o.selected = true
        }
    })
    
    siteForm.querySelectorAll("#font_size option").forEach(o => {
        if (o.value === site.font_size){
            o.selected = true
        }
    })

    siteForm.querySelector(".logo img").src = site.logo ? site.logo : '/static/account/images/baselogo.png'
    siteForm.querySelector(".logo img").style.width = site.logo ? site.logo_width : 'auto'

    siteForm.querySelector("input[name=logo_size]").value = site.logo ? site.width_percent : '100'
    siteForm.querySelector("input[name=owner]").value = site.owner ? site.owner : ''
    siteForm.querySelector("input[name=contact_info]").value = site.contact_info ? site.contact_info : ''
}

async function openSiteForm(){
    siteForm = document.querySelector(".site-form");

    fetch(`/get-change-site-form`)

    const response = await getSiteAPI()

    console.log(response.status)
   
    console.log(response)
    setSiteFormValues(response.data.site)
    initChangeSiteForm();
    openForm(siteForm);
}

const openSiteFormButton = document.querySelector("#open-site-form");
if (openSiteFormButton != null){
    openSiteFormButton.addEventListener("click", () => openSiteForm());
}

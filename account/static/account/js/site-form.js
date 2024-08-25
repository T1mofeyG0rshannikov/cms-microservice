function changeLogoSize(range){
    console.log(range.value);

    newLogoWidth = 260 * (range.value / 100);

    const image = document.querySelector("#logo img");
    image.style.width = newLogoWidth;
}

function onSubmitSiteForm(element, event){
    event.preventDefault();

    const data = new FormData(element);
    data.append('logo', element.querySelector("#file").files[0]);
    console.log(element.querySelector("#logo").querySelector("img").src)

    if (element.querySelector("#logo").querySelector("img").src === `${window.location.protocol}//${window.location.host}/static/account/images/baselogo.png`){
        data.append('delete_logo', true);
    }
    else{
        data.append('delete_logo', false);
    }

   const token = getToken();

    fetch(`/my/change-site`, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': `${token}`,
        },
        body: data
    }).then(response => {
        if (response.status === 200){
            setErrors({}, element)
            console.log("success");
            window.history.replaceState(null, '', window.location.pathname);
            location.reload();
        }
        if (response.status === 401){
            window.location.href="/user/login";
        }
        return response.json();
    }).then(response => {
        console.log(response.errors);
        setErrors({}, element)
        setErrors(response.errors, element)
    })
}


function initChangeSiteForm(){
    siteForm = document.querySelector(".site-form");

    const range = siteForm.querySelector("input[type=range]");
    range.addEventListener("input", () => changeLogoSize(range))

    const logo = siteForm.querySelector("#logo")
    const logoLoader = logo.querySelector("#file");

    logoLoader.addEventListener("change", () => displayPhotoOnload(logo))
}

function deleteLogo(){
    siteForm.querySelector("#logo img").src = "/static/account/images/baselogo.png"
    siteForm.querySelector("#logo input").value = "";

    siteForm.querySelector("input[type=range]").value = 100;
    changeLogoSize(siteForm.querySelector("input[type=range]"));
}

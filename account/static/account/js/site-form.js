function changeLogoSize(range){
    console.log(range.value);

    newLogoWidth = 260 * (range.value / 100);

    const image = document.querySelector("#logo img");
    image.style.width = newLogoWidth;
}

function onSubmitSiteForm(domain, element, event){
    event.preventDefault();

    const data = new FormData(element);
    data.append('logo', document.getElementById("file").files[0])

    const socialContainers = element.querySelector("#socials").querySelectorAll(".field-container");

    let socials = [];

    for (let socialContainer of socialContainers){
        let social = socialContainer.querySelector(".social").querySelector("select").value;
        let adress = socialContainer.querySelector("input[name=adress]").value;

        if (social.length > 0 && adress.length > 0){
            socials.push({social: social, adress: adress});
        }
    }
    const token = getToken();

    console.log(socials);
    data.append("socials", JSON.stringify(socials));
    console.log(data);

    fetch(`http://${domain}/my/change-site`, {
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
            location.reload();
        }
        if (response.status === 401){
            window.location.href="/user/login";
        }
        return response.json();
    }).then(response => {
        setErrors({}, element)
        setErrors(response.errors, element)
    })
}

function getSocialOptions(){
    let socialOptions = document.querySelector("#socials").querySelector("select").querySelectorAll("option")
    let socialValues = [""];
    let socialTexts = ["Выбрать"];

    for (let socialOption of socialOptions){
        if (socialOption.value.length > 0){
            socialValues.push(socialOption.value);
            socialTexts.push(socialOption.innerText);
        }
    }

    let options = '';

    for (let i = 0; i < socialValues.length; i++){
        options += `<option value="${socialValues[i]}">${socialTexts[i]}</option>`;
    }

    return options
}

function createNewSocial(){
    const options = getSocialOptions()

    const newSocial = document.createElement("div")
    newSocial.classList.add("field-container");
    newSocial.innerHTML = `
    <div class="field social">
        <p>Соцсеть</p>
        <select name="" id="">
            ${options}
        </select>
    </div>

    <div class="field adress">
        <p>Адрес</p>
        <input name="adress" />
    </div>

    <div class="trash-container">
        <img class="trash" onclick="deleteSocial(this)" src="/static/account/images/trash.png"/>
    </div>
    `

    return newSocial;
}

function observableNewSocials(){
    const socials = document.querySelector("#socials");
    const socialAdresses = socials.querySelectorAll("input[name=adress]");

    for (let input of socialAdresses){
        input.addEventListener("change", () => {
            const socialsCount = document.querySelector("#socials").querySelectorAll("input[name=adress]").length;
            const currIndex = [...socialAdresses].indexOf(input)

            if (currIndex === socialsCount - 1 && socialsCount < 4){
                const newSocial = createNewSocial();

                socials.appendChild(newSocial);
                observableNewSocials();
            }
        });
    }
}

function deleteSocial(element){
    const newSocial = createNewSocial();

    const socials = document.querySelector("#socials");
    const trashes = socials.querySelectorAll(".trash");

    const currentIndex = [...trashes].indexOf(element);

    const social = socials.querySelectorAll(".field-container")[currentIndex];
    social.remove();

    if (trashes.length === 1){
        socials.appendChild(newSocial);
        observableNewSocials();
    }
}


function initChangeSiteForm(){
    siteForm = document.querySelector(".site-form");

    const range = siteForm.querySelector("input[type=range]");
    range.addEventListener("input", () => changeLogoSize(range))

    const logo = siteForm.querySelector("#logo")
    const logoLoader = logo.querySelector("#file");

    logoLoader.addEventListener("change", () => displayPhotoOnload(logo))

    observableNewSocials();
}

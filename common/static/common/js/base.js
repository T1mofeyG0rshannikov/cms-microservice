function openLink(url){
    window.open(url)
}

function displayPhotoOnload(element) {
    const imageLoader = element.querySelector("#file");
    const file = imageLoader.files[0];
    const reader  = new FileReader();

    reader.onload = function(e)  {
        const image = element.querySelector("img");
        image.src = e.target.result;
    }

    reader.readAsDataURL(file);
}

const userNav = document.querySelector(".user-nav");

function closeForm(form){
    $(document.querySelector(".user-nav")).removeAttr("style");

    form.style.right = "-480px";
}

function closeUserNav(){
    document.querySelector(".user-nav").style.display = "none";

    setTimeout(() => $(document.querySelector(".user-nav")).removeAttr("style"), 1000);
}

function openForm(form){
    const forms = document.querySelectorAll(".form");
    for (let formElem of forms){
        closeForm(formElem);
    }

    closeUserNav();
    resetForm(form);
    form.style.right = "0px";
}

function resetForm(element){
    const inputs = element.querySelectorAll("input");

    for (let input of inputs){
        if ($(input).attr("default") !== undefined){
            console.log(input);
            input.value = $(input).attr("default");
        }
    }
}

function closeFormPopup(popup){
    popup.style.display = "none";
}

function openFormPopup(popup){
    popup.style.animation = "auto";
    const popups = document.querySelectorAll(".form-container");

    for (let popupElem of popups){
        closeFormPopup(popupElem);
    }

    popup.style.display = "flex";
}

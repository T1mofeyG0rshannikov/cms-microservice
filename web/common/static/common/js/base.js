function openLink(url, product_id, type="link"){
    window.open(url);
    fetch(`/site_statistics/opened-product-${type}?product_id=${product_id}`)
}

function displayPhotoOnload(element) {
    const imageLoader = element.querySelector("input[type=file]");
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

    form.style.right = "-560px";
}

function closeUserNav(){
    if (document.querySelector(".user-nav")){
        document.querySelector(".user-nav").style.display = "none";
    }

    setTimeout(() => $(document.querySelector(".user-nav")).removeAttr("style"), 1000);
}

function removeFormErrors(popup){
    for (let field of popup.querySelectorAll(".field")){
        setError(field, "")
    }
}

function openForm(form){
    const forms = document.querySelectorAll(".form");
    for (let formElem of forms){
        closeForm(formElem);
    }

    closeUserNav();
    removeFormErrors(form);
    form.style.right = "0px";
}

function closeFormPopup(popup){
    for (let input of popup.querySelectorAll("input")){
        if ($(input).attr("type") != "submit"){
            if ($(input).attr("name") != "csrfmiddlewaretoken"){
                input.value = "";
            }
        }
    }

    removeFormErrors(popup)
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

function openTextPopup(element){
    element.style.display = "block";
}

function closeTextPopup(element){
    document.body.removeChild(element)
}

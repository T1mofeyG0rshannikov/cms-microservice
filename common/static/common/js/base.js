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

function closeForm(form){
    form.style.right = "-480px";
}

function openForm(form){
    const forms = document.querySelectorAll(".form");
    for (let formElem of forms){
        closeForm(formElem);
    }

    form.style.right = "30px";
}

function openPopup(product_id){
    const popup = document.querySelectorAll(".product")[product_id - 1].querySelector(".popup-background");
    popup.style.display = "block";
}

function closePopup(product_id){
    const popup = document.querySelectorAll(".product")[product_id - 1].querySelector(".popup-background");
    popup.style.display = "none";
}

const popupBackgrounds = document.querySelectorAll(".popup-background")

popupBackgrounds.forEach((popup, index) => {
    popup.addEventListener("mousedown", event => {
        if (!popup.querySelector(".description-popup").contains(event.target)){
            closePopup(index + 1);
        }
    })
})

function openProductLink(url){
    window.open(url)
}

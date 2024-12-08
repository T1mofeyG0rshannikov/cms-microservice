document.querySelectorAll(".form-container").forEach(form => {
    form.addEventListener("mousedown", event => {
        if (!form.querySelector("form").contains(event.target)){
            closeFormPopup(form);
        }
    })
})

$(document).keyup(function(e) {
    if (e.key === "Escape"){
        const popups = document.querySelectorAll(".form-container")
        for (let popup of popups){
            closeFormPopup(popup);
        }
   }
});

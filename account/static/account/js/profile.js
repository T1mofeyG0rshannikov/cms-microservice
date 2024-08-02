document.querySelectorAll(".form-container").forEach(form => {
    form.addEventListener("mousedown", event => {
        if (!form.querySelector("form").contains(event.target)){
            closeFormPopup(form);
        }
    })
})

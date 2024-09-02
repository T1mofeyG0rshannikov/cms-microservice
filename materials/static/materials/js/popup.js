function openDocumentPopup(documentSlug){
    fetch(`/materials/popup?document=${documentSlug}`).then(response => response.json()).then(response => {
        const popup = document.createElement('div');
        document.body.appendChild(popup);
        console.log(popup);
        popup.outerHTML = response.content;
        const element = document.querySelector(".document-popup")
        openTextPopup(element);
    })
}

function closeDocumentPopup(){
    const popup = document.querySelector(".document-popup");
    closeTextPopup(popup);
}

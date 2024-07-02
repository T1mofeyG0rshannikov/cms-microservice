const range = document.querySelector("input[type=range]");

function changeLogoSize(){
    console.log(range.value);
}

range.addEventListener("input", changeLogoSize)

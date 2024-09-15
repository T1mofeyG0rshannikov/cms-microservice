function openQuestion(id){
    const question = document.querySelectorAll(".question")[id - 1];
    question.querySelector("span").style.display = "block";

    question.querySelector(".title").removeEventListener("click", () => {
        openQuestion(id)
    })

    question.querySelector(".title").addEventListener("click", () => {
        closeQuestion(id)
    })
    question.querySelector("img").outerHTML = `<img src="static/blocks/images/triangle-reverse.png"/>`
}

function closeQuestion(id){
    const question = document.querySelectorAll(".question")[id - 1];
    question.querySelector("span").style.display = "none";

    question.querySelector(".title").removeEventListener("click", closeQuestion)

    question.querySelector(".title").addEventListener("click", () => {
        openQuestion(id)
    })
    question.querySelector("img").outerHTML = `<img src="static/blocks/images/triangle.png"/>`
}

function successSendFeedback(element){
    element.querySelector("h3").innerHTML = "Сообщение отправлено";
    element.querySelector(".fields").innerHTML = "<p style='color: var(--main-text-color);'>Мы постараемся ответить на ваш запрос в течение 1-2 рабочих дней.</p>";
}


function submitFeedbackForm(element, event){
    event.preventDefault();

    const data = new FormData(element);

    fetch(`/feedback`, {
        method: "post",
        withCredentials: true,
        headers: {
            'Accept': 'application/json',
            'X-CSRFToken': data.get("csrfmiddlewaretoken")
        },
        body: data
    }).then(response => {
        if (response.status === 200){
            successSendFeedback(element)
        }
        return response.json();
    }).then(response => {
        const errors = response.errors;

        const fields = element.querySelectorAll(".field");

        for (let field of fields){
            setError(field, "")
        }

        for (let field of Object.keys(errors)) {
            setError(element.querySelector(`#${field}`), errors[field][0]);
        }
    })
}

function submitRegisterForm(element, event){
    event.preventDefault();

    const data = new FormData(element);

    fetch("/user/register", {
        method: "post",
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': data.get("csrfmiddlewaretoken"),
        },
        body: data
    }).then(response => {
        if (response.status === 200){
            response.json().then((response) => {
                const token_to_set_password = response.token_to_set_password;
                window.location.replace(`/user/password/${token_to_set_password}`)
            })
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

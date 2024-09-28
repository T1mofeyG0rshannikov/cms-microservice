function submitRegisterForm(element, event, domain, ancor=null, is_popup=false){
    event.preventDefault();

    const data = new FormData(element);
    data.append("ancor", ancor);
    data.append("is_popup", is_popup);

    fetch(`/user/register`, {
        method: "post",
        withCredentials: true,
        headers: {
            'Accept': 'application/json',
            'X-CSRFToken': data.get("csrfmiddlewaretoken")
        },
        body: data
    }).then(response => {
        if (response.status === 200){
            response.json().then((response) => {
                const token_to_set_password = response.token_to_set_password;
                window.location.replace(`${window.location.protocol}//${domain}/user/password/${token_to_set_password}`)
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

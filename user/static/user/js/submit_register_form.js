function submitRegisterForm(element, event){
    event.preventDefault();

   /* const form = document.querySelector(".user-form")*/
    const data = new FormData(element);

    fetch("/user/register", {
        method: "post",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify({
            "csrfmiddlewaretoken": data.get("csrfmiddlewaretoken"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "username": data.get("username")
        })
    }).then(response => {
        if (response.status === 200){
            response.json().then((response) => {
                const token_to_set_password = response.token_to_set_password;
                console.log(token_to_set_password);
                window.location.replace(`/user/password/${token_to_set_password}`)
            })
        }
        return response.json();
    }).then(response => {
        const errors = response.errors;
        setError(element.querySelector(`#username`), "")
        setError(element.querySelector(`#phone`), "")
        setError(element.querySelector(`#email`), "")
        //console.log(errors);
        for (let field of Object.keys(errors)) {
            /*console.log(field, errors[field], "field");
            console.log(element.querySelector(`#${field}`))*/
            setError(element.querySelector(`#${field}`), errors[field][0]);
        }
    })
}

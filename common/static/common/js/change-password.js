const changePasswordForm = document.querySelector(".change-password-form");

function onSubmitChangePasswordForm(element, event){
    event.preventDefault();

    const data = new FormData(element);
    const token = getToken();

    console.log(data);

    fetch(`/my/change-password`, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': `${token}`,
        },
        body: data
    }).then(response => {
        if (response.status === 200){
            setErrors({}, element)
            console.log("success");
            location.reload();
        }
        return response.json();
    }).then(response => {
        setErrors({}, element)
        setErrors(response.errors, element)
    })
}

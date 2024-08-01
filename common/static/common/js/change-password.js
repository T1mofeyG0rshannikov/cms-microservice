const changePasswordForm = document.querySelector(".change-password-form");

function onSubmitChangePasswordForm(domain, element, event){
    event.preventDefault();

    const data = new FormData(element);
    const token = getToken();

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
            const access_token = response.json().access_token;
            setToken(access_token);
            closeForm(changePasswordForm);

            window.location.replace(`http://${domain}/user/set-token/${token}`);
            return;
        }
        return response.json();
    }).then(response => {
        setErrors({}, element)
        setErrors(response.errors, element)
    })
}

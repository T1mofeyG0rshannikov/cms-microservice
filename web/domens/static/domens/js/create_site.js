function submitCreateSiteForm(element, event, domain){
    event.preventDefault();

    const data = new FormData(element);
    data.append('logo', document.getElementById("id_logo").files[0])
    data.append('logo2', document.getElementById("id_logo2").files[0])

    const token = getToken();

    fetch(`${window.location.protocol}//${domain}/domain/create-site`, {
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
        }
        return response.json();
    }).then(response => {
        setErrors(response.errors, element)
    })
}

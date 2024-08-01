function onSubmitChangeUserForm(element, event){
    event.preventDefault();

    const data = new FormData(element);
    const token = getToken();

    fetch(`/my/change-user`, {
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
        if (response.status === 401){
            window.location.href = "/user/login?next=my/site";
        }
        return response.json();
    }).then(response => {
        setErrors({}, element)
        setErrors(response.errors, element)
    })
}

let changeUserForm = document.querySelector(".change-user-form");

function initChangeUserForm(){
    changeUserForm = document.querySelector(".change-user-form");

    const userLogo = changeUserForm.querySelector(".user-logo");
    const userLogoLoader = userLogo.querySelector("#file");

    userLogoLoader.addEventListener("change", () => displayPhotoOnload(userLogo));

    const emailInput = changeUserForm.querySelector("input[name=email]");
    const phoneInput = changeUserForm.querySelector("input[name=phone]");

    emailInput.addEventListener("change", () => {
        validEmail = onchangeEmail(changeUserForm);
    });

    $("input[name=phone]").mask("+7 (999) 999-99-99")
    $("input[name=phone]").on("change", () => {
        validPhone = onchangePhone(changeUserForm);
    })
}

initChangeUserForm();

function sendConfirmEmail(){
    const token = getToken();

    fetch(`/email/send-confirm-email`, {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': `${token}`,
        }
    }).then(response => {
        if (response.status === 200){
            console.log("success")
        }
    })
}

function openUserForm(form){
    const userLogo = form.querySelector(".user-logo img");
    userLogo.src = $(userLogo).attr("default");
    form.querySelector("#file").value = "";

    fetch(`/get-change-user-form`).then(response => response.json()).then(response => {
        form.innerHTML = response.content;
        initChangeUserForm();
        openForm(form);
    })
}

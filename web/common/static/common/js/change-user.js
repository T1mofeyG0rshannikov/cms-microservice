function onSubmitChangeUserForm(element, event){
    event.preventDefault();

    const data = new FormData(element);
    data.append('profile_picture', element.querySelector("#file").files[0])
    console.log(element.querySelector("#file").files[0]);
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
            window.history.replaceState(null, '', window.location.pathname);
            location.reload();
        }
        if (response.status === 401){
            window.location.href = "/user/login?next=my/site";
        }
        return {
            json: response.json(),
            status: response.status
        };
    }).then(response => {
        if (response.status === 400){
            response.json.then(res => {
                setErrors({}, element)
                setErrors(res.errors, element)
            });
        }
        else if (response.status === 202){
            response.json.then(res => {
                window.history.replaceState(null, '', window.location.pathname + `?info_title=${res.info.title}&info_text=${res.info.text}`);
                location.reload();
            })
        }
    })
}

let changeUserForm = document.querySelector(".change-user-form");

function initChangeUserForm(){
    changeUserForm = document.querySelector(".change-user-form");

    const userLogo = changeUserForm.querySelector(".user-logo");
    const userLogoLoader = userLogo.querySelector("#file");

    userLogoLoader.addEventListener("change", () => displayPhotoOnload(userLogo));

    const emailInput = changeUserForm.querySelector("input[name=email]");

    emailInput.addEventListener("change", () => {
        validEmail = onchangeEmail(changeUserForm);
    });

    $("input[name=phone]").mask("+7 (999) 999-99-99")
    $("input[name=phone]").on("change", () => {
        validPhone = onchangePhone(changeUserForm);
    })
}

initChangeUserForm();

function sendConfirmEmail(elem){
    const token = getToken();
    elem.innerHTML = "Отправляем письмо...";
    elem.style.color = "var(--main-text-color)";

    fetch(`/email/send-confirm-email`, {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': `${token}`,
        }
    }).then(response => {
        if (response.status === 200){
            elem.innerHTML = "Ссылка отправлена на email";
            console.log("success")
        }
        if (response.status === 503){
            response.json().then(response => {
                elem.style.color = "rgb(250, 20, 20)";
                elem.innerHTML = response.error;
            })
        }
    })
}

function getUserForm(){
    return document.querySelector(".change-user-form")
}

function openUserForm(form=getUserForm()){
    fetch(`/get-change-user-form`).then(response => response.json()).then(response => {
        form.innerHTML = response.content;
        initChangeUserForm();
        openForm(form);
    })
}

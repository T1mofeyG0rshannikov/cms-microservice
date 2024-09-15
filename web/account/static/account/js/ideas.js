function getIdeaImage(idea, user_id){
    console.log(idea, user_id, idea.user_id, idea.user_icon)
    if (user_id === idea.user_id){
        if (idea.user_icon !== null){
            return `<img src="${ idea.user_icon }" />`;
        }

        return `<img src="/static/account/images/nophoto.jpg" />`;
    }

    if (idea.category === "errors"){
        return `<img src="/static/account/images/bugs/icobug_error.png" />`;
    }
    else if (idea.category === "correction"){
        return `<img src="/static/account/images/bugs/icobug_fix.png" />`;
    }

    else if (idea.category === "modernization"){
        return `<img src="/static/account/images/bugs/icobug_addon.png" />`;
    }
    else if (idea.category === "new_feature"){
        return `<img src="/static/account/images/bugs/icobug_idea.png" />`;
    }
}

function renderIdeas(ideas, user_id){
    let ideasHTML = '';
    for (let idea of ideas){
        let ideaHTML = `
        <tr style="border-bottom: 1px solid var(--dark-color);">
            <td style="width: 40px;" class="status">
                ${getIdeaImage(idea, user_id)}
            </td>

            <td style="width: 90px;">${ idea.created_at }</td>
            <td>
                <p class="change-idea">
                    <span class="fw600">
                        ${ idea.title }
                    </span>

                    ${ idea.status == "Новое" ? (
                        idea.user_id == user_id ? (
                            `<img title="Настройка" onclick="openUpdateIdeaForm(${ idea.id })" src="/static/account/images/icoint_edit.png" />`
                        ): ''
                        ): ''
                    }
                </p>

                <div>
                    <span onclick="openIdeaDescription(this)" class="description hidden">
                        ${ idea.description }

                        ${ idea.admin_answer ? (
                            `<br />
                            <br />
                            <span style="font-style: italic;">Ответ администрации:</span>
                            ${ idea.admin_answer }`
                        ): ''
                    }
                    </span>
                </div>
            </td>

            <td style="width: 140px; padding-left: 30px;">${ idea.user }</td>
            <td style="width: 120px;">${ idea.status }</td>
            <td style="width: 120px;">${ idea.finishe_date }</td>

            <td style="width: 100px;">
                <div class="like">
                    <img onclick="addLike(this, ${idea.id})" src="${idea.liked ? "/static/account/images/bugs/icobug_yes.png" : "/static/account/images/bugs/icobug_vote.png"}" />
                    <span>${ idea.likes_count }</span>
                </div>
            </td>
        </tr>
        `;

        ideasHTML += ideaHTML;
    }

    document.querySelector("tbody").innerHTML = ideasHTML;
}


function loadIdeas(page=1){
    const category = $("select[name=category]").val();
    const status = $("select[name=status]").val();
    const sorted_by = $("select[name=sort_by]").val();
    const page_size = $("select[name=page_size]").val();

    fetch(`/user/ideas?category=${category}&page_size=${page_size}&status=${status}&page=${page}&sorted_by=${sorted_by}`).then(response => {
        if (response.status === 200){
            response.json().then(response => {
                renderIdeas(response.ideas, response.user_id);
                renderPagination(page, response.total_pages, 'loadIdeas');
                rememberIdeasFilters();
                changePaginationCount(response.count);
            })
        }
    })
}

function openIdeaForm(){
    createIdeaForm = document.querySelector(".create-idea-form");

    fetch(`/get-create-idea-form`).then(response => response.json()).then(response => {
        createIdeaForm.innerHTML = response.content;
        openForm(createIdeaForm);
        initCreateIdeaForm();
        addScreensLoadEvent();
    })
}

let createIdeaForm = document.querySelector(".create-idea-form");

function onSubmitCreateIdeaForm(element, event, ideaId){
    event.preventDefault();

    const data = new FormData(element);
    let screensSrc = [];

    for (let screen of element.querySelectorAll("input[type=file]")){
        if (screen.files[0] !== undefined){
            data.append('screens', screen.files[0])
            screensSrc.push(screen.files[0].name);
        }
    }

    for (let screen of element.querySelectorAll(".screens-container .field img")){
        if (!screen.src.includes('data:image')){
            const screenSrc = screen.src.split("/")[screen.src.split("/").length - 1];
            if (screenSrc !== 'noscreen.jpg'){
                screensSrc.push(screenSrc)
            }
        }
    }

    data.append('screensSrc', screensSrc);

    if (ideaId === undefined){
        fetch(`/user/idea`, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: data
        }).then(response => {
            if (response.status === 201){
                setErrors({}, element)
                console.log("success");
                window.history.replaceState(null, '', window.location.pathname);
                location.reload();
            }
            if (response.status === 401){
                window.location.href="/user/login";
            }
            return response.json();
        }).then(response => {
            setErrors({}, element)
            setErrors(response.errors, element)
        })
    }

    else{
        fetch(`/user/update-idea?idea=${ideaId}`, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: data
        }).then(response => {
            if (response.status === 201){
                setErrors({}, element)
                console.log("success");
                window.history.replaceState(null, '', window.location.pathname);
                location.reload();
            }
            if (response.status === 401){
                window.location.href="/user/login";
            }
            return response.json();
        }).then(response => {
            setErrors({}, element)
            setErrors(response.errors, element)
        })
    }
}

function initCreateIdeaForm(){
    createIdeaForm = document.querySelector(".create-idea-form");

    createIdeaForm.querySelector(".cross img").addEventListener('click', closeCreateProductForm);

    createIdeaForm.addEventListener('submit', event => onSubmitCreateIdeaForm(createIdeaForm, event))
}


function rememberIdeasFilters(){
    const url = new URL(window.location.href);

    const category = $("select[name=category]").val();
    url.searchParams.set('category', category);

    const page_size = $("select[name=page_size]").val();
    url.searchParams.set('page_size', page_size);

    const status = $("select[name=status]").val();
    url.searchParams.set('status', status);

    window.history.replaceState(null, '', window.location.pathname + url.search);
}

function addScreen(){
    const screensCount = document.querySelectorAll('.screens-container input[type=file]').length;

    let screen =
    `
    <div id="file${screensCount + 1}" class="screen field">
        <div class="screen-image">
            <img src="/static/account/images/noscreen.jpg" alt="скриншот">
            <input name="file" type="file" accept="image/*" />
        </div>
    </div>`;

    if (screensCount < 2){
        screen += `<button onclick="addScreen()" class="br50">+</button>`;
    }

    const screenContainer = createIdeaForm.querySelector(".screens-container");
    const button = screenContainer.querySelector("button");
    screenContainer.removeChild(button);
    screenElem = document.createElement('div');
    screenContainer.appendChild(screenElem);
    screenElem.outerHTML = screen;

    screenContainer.scrollLeft = screenContainer.scrollWidth;

    addScreensLoadEvent();
}

function addScreensLoadEvent(){
    const screens = createIdeaForm.querySelectorAll(".screen");

    screens.forEach(screen => {
        const screenLoader = screen.querySelector("input[type=file]");
        screenLoader.addEventListener("change", () => displayPhotoOnload(screen));
    })
}

function openIdeaDescription(element){
    const isTextClamped =  element.scrollHeight > element.clientHeight;

    if (!isTextClamped){
        return;
    }

    element.classList.remove("hidden")

    element.style.cursor = 'auto';
    const a = document.createElement("a");

    element.parentElement.appendChild(a);
    a.outerHTML = `<a style="color: var(--light-ref-color); cursor: pointer;">скрыть</a>`
    element.parentElement.querySelector("a").addEventListener('click', () => hideIdeaDescription(element.parentElement))
    element.style.pointerEvents = "none";
}

function hideIdeaDescription(element){
    element.querySelector(".description").classList.toggle("hidden");

    element.querySelector(".description").style.cursor = "pointer";
    element.querySelector(".description").style.pointerEvents = "auto";

    const a = element.querySelector("a")
    element.removeChild(a);
}

function addLike(element, ideaId){
    if (element.src.split("/")[element.src.split("/").length - 1] === "icobug_vote.png"){
        fetch(`/user/like?idea=${ideaId}`, {method: "POST"}).then(response => {
            if (response.status === 201){
                element.src = "/static/account/images/bugs/icobug_yes.png";
                element.parentElement.querySelector("span").innerHTML = Number(element.parentElement.querySelector("span").innerHTML) + 1
            }
        })
    }
    else{
        fetch(`/user/like?idea=${ideaId}`, {method: "DELETE"}).then(response => {
            if (response.status === 204){
                element.src = "/static/account/images/bugs/icobug_vote.png";
                element.parentElement.querySelector("span").innerHTML = Number(element.parentElement.querySelector("span").innerHTML) - 1
            }
        })
    }
}

function initIdeas(){
    if (document.querySelector("select[name=category") != null){
        document.querySelector("select[name=category").addEventListener("change", () => loadIdeas());
        document.querySelector("select[name=status").addEventListener("change", () => loadIdeas());
        document.querySelector("select[name=sort_by").addEventListener("change", () => loadIdeas());
        document.querySelector("select[name=page_size]").addEventListener("change", () => loadIdeas());
    }
}

function createIdeaFormremoveEventListeners(){
    createIdeaForm.removeEventListener('submit', onSubmitCreateIdeaForm)
    createIdeaForm.removeEventListener('submit', onSubmitUpdateIdeaForm)
}

function openUpdateIdeaForm(ideaId){
    createIdeaForm = document.querySelector(".create-idea-form");

    fetch(`/get-create-idea-form?idea=${ideaId}`).then(response => response.json()).then(response => {
        createIdeaForm.outerHTML = response.content;
        createIdeaForm = document.querySelector(".create-idea-form");
        openForm(createIdeaForm);
        initUpdateIdeaForm(ideaId);
        addScreensLoadEvent();
    })
}

function onSubmitUpdateIdeaForm(element, event, ideaId){
    event.preventDefault();

    const data = new FormData(element);
    let screens = [];

    for (let screen of element.querySelectorAll("input[type=file]")){
        if (screen.files[0] !== undefined){
            data.append('screens', screen.files[0])
        }
    }

    fetch(`/user/update-idea?idea=${ideaId}`, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: data
    }).then(response => {
        if (response.status === 201){
            setErrors({}, element)
            console.log("success");
            window.history.replaceState(null, '', window.location.pathname);
            location.reload();
        }
        if (response.status === 401){
            window.location.href="/user/login";
        }
        return response.json();
    }).then(response => {
        setErrors({}, element)
        setErrors(response.errors, element)
    })
}

function initUpdateIdeaForm(ideaId){
    createIdeaForm = document.querySelector(".create-idea-form");

    createIdeaForm.querySelector(".cross img").addEventListener('click', closeCreateProductForm);
}


function deleteIdea(ideaId){
    fetch(`/user/delete-idea?idea=${ideaId}`, {method: "DELETE"}).then(response => {
        if (response.status === 204){
            console.log("success")
            window.location.reload()
        }
    })
}

function renderProducts(products){
    let productsHTML = '';
    for (let product of products){
        productsHTML +=
        `<div class="product" onclick="choiceProduct(${ product.id })">
            <img src="${ product.image }" alt="${ product.name }">
            <div>
                <p>${ product.name }</p>
                <p>${ product.organization }</p>
            </div>
        </div>`;
    }

    choiceProductForm.querySelector('.products').innerHTML = productsHTML.length > 0 ? productsHTML : `<p>Нет финансовых продуктов</p>`;
}

function loadProducts(organizationId){
    fetch(`/products?organization=${organizationId}`).then(response => response.json()).then(response => {
        console.log(response.products);
        renderProducts(response.products);
    })
}

function openProductForm(){
    choiceProductForm = document.querySelector(".choice-product-form");

    fetch(`/get-choice-product-form`).then(response => response.json()).then(response => {
        choiceProductForm.innerHTML = response.content;
        openForm(choiceProductForm);

        choiceProductForm.querySelector('select[name=organization]').addEventListener('change', (event) => {
            loadProducts(event.target.value)
        })
    })
}

let choiceProductForm = document.querySelector(".choice-product-form");
let createProductForm = document.querySelector(".create-product-form");

function choiceProduct(productId){
    createProductForm = document.querySelector(".create-product-form");

    fetch(`/get-create-user-product-form?product=${productId}`).then(response => response.json()).then(response => {
        createProductForm.outerHTML = response.content;
        createProductForm = document.querySelector(".create-product-form");
        closeForm(choiceProductForm)
        openForm(createProductForm);
        initCreateProductForm();
    })
}

function onSubmitCreateUserProductForm(element, event, product){
    event.preventDefault();

    const data = new FormData(element);
    if (element.querySelector("#file").files[0] !== undefined){
        data.append('screen', element.querySelector("#file").files[0]);
    }

    data.append('product', product)
    data.append('connected_with_link', element.querySelector("input[name=connected_with_link]").checked);

   const token = getToken();

    fetch(`/my/add-user-product`, {
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
            window.location.href="/user/login";
        }
        return response.json();
    }).then(response => {
        console.log(response.errors);
        console.log(element);
        setErrors({}, element)
        setErrors(response.errors, element)
    })
}

function initCreateProductForm(){
    createProductForm = document.querySelector(".create-product-form");

    const screen = createProductForm.querySelector(".photo")
    const screenLoader = screen.querySelector("#file");

    screenLoader.addEventListener("change", () => displayPhotoOnload(screen))
}

function changeProductLink(event){
    createProductForm.querySelector("#copy_link").addEventListener("click", () => {
        navigator.clipboard.writeText(event.target.value).then(() => {
            console.log("success")
        })
    })

    createProductForm.querySelector("#go_link").addEventListener("click", () => {
        openLink(event.target.value);
    })
}

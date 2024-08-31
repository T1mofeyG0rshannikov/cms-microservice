function renderUserProducts(products){
    let productsHTML = '';
    for (let user_product of products){
        const productHTML = `
        <tr>
            <td class="product">
                <img src="${ user_product.product.image }" />

                <div>
                    <p>${ user_product.product.name }</p>
                    <p>${ user_product.product.organization }</p>
                </div>
            </td>

            <td>${ user_product.end_promotion }</td>
            <td>${ user_product.created }</td>
            <td>${ user_product.gain }</td>
            <td>${ user_product.redirections }</td>

            <td>
                <div class="icons">
                    <img src="/static/account/images/settings.png" />
                    <img src="/static/account/images/icoint_stat.png" />
                    <img src="/static/account/images/icoint_doc.png" />
                    <img src="/static/account/images/icoint_del.png" />
                </div>
            </td>
        </tr>
        `;

        productsHTML += productHTML;
    }

    document.querySelector("tbody").innerHTML = productsHTML;
}

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

function loadUserProducts(page=1){
    const category = $("select[name=category]").val();
    const page_size = $("select[name=page_size]").val();
    const date = $("select[name=date]").val();

    fetch(`/user-products?category=${category}&page_size=${page_size}&date=${date}&page=${page}`).then(response => {
        if (response.status === 200){
            response.json().then(response => {
                console.log(response);
                renderUserProducts(response.products);
                console.log(response.total_pages);
                renderProductsPagination(page, response.total_pages);
                rememberProductsFilters();
                changePaginationCount(response.count);
            })
        }
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

function showAdditionalFields(){
    if (createProductForm.querySelector("input[type=checkbox]").checked){
        document.querySelector(".additional-fields").style.display = "block";
    }
    else{
        document.querySelector(".additional-fields").style.display = "none";
    }
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


function initUserProducts(){
    document.querySelector("select[name=category").addEventListener("change", () => loadUserProducts());
    document.querySelector("select[name=page_size]").addEventListener("change", () => loadUserProducts());
}


function renderProductsPagination(pageNum, totalPages){
    let pagination = `<a ${ pageNum == 1 ? 'class="active"' : "" } onclick="loadUserProducts(1)">1</a>`;

    if (pageNum > 4){
        pagination += `...`;
    }

    if (pageNum == 1){
        for (let num = 1; num <= totalPages; num++){
            if (pageNum < num && num < pageNum + 3){
                if (num != 1 && num != totalPages){
                    pagination += `<a ${ num == pageNum ? 'class="active"' : "" } onclick="loadUserProducts(${ num })">${ num }</a>`;
                }
            }
        }
    }

    else if (pageNum == totalPages){
        for (let num = 1; num <= totalPages; num++){
            if (pageNum-3 < num && num < pageNum){
                if (num != totalPages && num != 1){
                    pagination += `<a ${ num == pageNum ? 'class="active"' : "" } onclick="loadUserProducts(${ num }, ${totalPages})">${ num }</a>`;
                }
            }
        }
    }
    else{
        for (let num =1; num <= totalPages; num++){
            if (pageNum-2 < num && num < pageNum + 2){
                if (num != totalPages && num != 1){
                    pagination += `<a ${ num == pageNum ? 'class="active"' : "" } onclick="loadUserProducts(${ num }, ${totalPages})">${ num }</a>`;
                }
            }
        }
    }

    if (pageNum < totalPages - 3){
        pagination += `...`;
    }

    if (totalPages > 1){
        pagination += `<a ${ pageNum == totalPages ? 'class="active"' : "" } onclick="loadUserProducts(${ totalPages }, ${totalPages})">${ totalPages }</a>`;
    }

    if (totalPages > 1){
        document.querySelector(".pages").innerHTML = pagination;
    }
    else{
        document.querySelector(".pages").innerHTML = '';
    }
}

function rememberProductsFilters(){
    const url = new URL(window.location.href);

    const category = $("select[name=category]").val();
    url.searchParams.set('category', category);

    const page_size = $("select[name=page_size]").val();
    url.searchParams.set('page_size', page_size);

    const date = $("select[name=date]").val();
    url.searchParams.set('date', date);

    window.history.replaceState(null, '', window.location.pathname + url.search);
}

function addPageToSearch(page){
    const url = new URL(window.location.href);

    url.searchParams.set('page', page);

    window.history.replaceState(null, '', window.location.pathname + url.search);
}

initUserProducts();

function closeCreateProductForm(){
    closeForm(createProductForm);
    openForm(choiceProductForm);
}

function openTextPopup(element){
    element.style.display = "block";
}

function openProductDescription(){
    const element = document.querySelector(".product-description")
    openTextPopup(element);
}

function closeTextPopup(element){
    element.style.display = "none";
}

function closeProductDescription(){
    const element = document.querySelector(".product-description");
    closeTextPopup(element);
}

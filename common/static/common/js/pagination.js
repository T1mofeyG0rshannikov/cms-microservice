function addPageToSearch(page){
    const url = new URL(window.location.href);

    url.searchParams.set('page', page);

    window.history.replaceState(null, '', window.location.pathname + url.search);
}


function changePaginationCount(count){
    document.querySelector(".pagination-count a").innerHTML = count
}


function renderPagination(pageNum, totalPages, changeFuncName){
    let pagination = `<a ${ pageNum == 1 ? 'class="active"' : "" } onclick="${changeFuncName}(1)">1</a>`;

    if (pageNum > 4){
        pagination += `...`;
    }

    if (pageNum == 1){
        for (let num = 2; num < totalPages; num++){
            if (pageNum < num && num < pageNum + 3){
                pagination += `<a ${ num == pageNum ? 'class="active"' : "" } onclick="${changeFuncName}(${ num })">${ num }</a>`;
            }
        }
    }

    else if (pageNum == totalPages){
        for (let num = 2; num < totalPages; num++){
            if (pageNum-3 < num && num < pageNum){
                pagination += `<a ${ num == pageNum ? 'class="active"' : "" } onclick="${changeFuncName}(${ num }, ${totalPages})">${ num }</a>`;
            }
        }
    }
    else{
        for (let num = 2; num < totalPages; num++){
            if (pageNum-2 < num && num < pageNum + 2){
                pagination += `<a ${ num == pageNum ? 'class="active"' : "" } onclick="${changeFuncName}(${ num }, ${totalPages})">${ num }</a>`;
            }
        }
    }

    if (pageNum < totalPages - 3){
        pagination += `...`;
    }

    if (totalPages > 1){
        pagination += `<a ${ pageNum == totalPages ? 'class="active"' : "" } onclick="${changeFuncName}(${ totalPages }, ${totalPages})">${ totalPages }</a>`;
    }

    if (totalPages > 1){
        document.querySelector(".pages").innerHTML = pagination;
    }
    else{
        document.querySelector(".pages").innerHTML = '';
    }
}

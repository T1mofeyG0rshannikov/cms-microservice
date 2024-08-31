function addPageToSearch(page){
    const url = new URL(window.location.href);

    url.searchParams.set('page', page);

    window.history.replaceState(null, '', window.location.pathname + url.search);
}


function changePaginationCount(count){
    document.querySelector(".pagination-count a").innerHTML = count
}

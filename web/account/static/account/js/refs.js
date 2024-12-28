function renderRefs(refs){
    let refsHTML = '';
    for (let referral of refs){
        const refHTML = `
        <tr>
            <td class="ref"  onclick="getReferralPopup(${ referral.id })">
                <div class="logo br50 b1dc">
                    <img src="${ referral.profile_picture ? referral.profile_picture : '/static/account/images/nophoto.jpg' }" />
                </div>

                <p>${ referral.full_name }</p>
            </td>

            <td>${ referral.created_at }</td>
            <td>${ referral.level }</td>
            <td>${ referral.channel }</td>
            <td>${ referral.referrals }</td>
            <td>${ referral.redirections }</td>
            <td class="message"><img ${ referral.level != 1 ? 'class="inactive"' : "" } src="/static/account/images/my_msg.png" /></td>
        </tr>
        `;

        refsHTML += refHTML;
    }

    document.querySelector("tbody").innerHTML = refsHTML;
}


function rememberFilters(){
    const url = new URL(window.location.href);

    const level = $("select[name=level]").val();
    url.searchParams.set('level', level);

    const page_size = $("select[name=page_size]").val();
    url.searchParams.set('page_size', page_size);

    const sorted_by = $("select[name=sort_by").val();
    url.searchParams.set('sorted_by', sorted_by);

    window.history.replaceState(null, '', window.location.pathname + url.search);
}

function addPageToSearch(page){
    const url = new URL(window.location.href);

    url.searchParams.set('page', page);

    window.history.replaceState(null, '', window.location.pathname + url.search);
}

function loadPagination(pageNum){
    const level = $("select[name=level]").val();
    const page_size = $("select[name=page_size]").val();
    const sorted_by = $("select[name=sort_by]").val()

    fetch(`/my/get-referrals?level=${level}&page_size=${page_size}&page=${pageNum}&sorted_by=${sorted_by}`).then(response => {
        if (response.status === 200){
            response.json().then(response => {
                console.log(response);
                renderRefs(response.referrals);
                renderPagination(pageNum, response.total_pages, 'loadPagination');

                rememberFilters();
                addPageToSearch(pageNum);
                changePaginationCount(response.count);
            })
        }
    })
}

function initRefsContent(){
    document.querySelector("select[name=level]").addEventListener("change", () => {
        const level = $("select[name=level]").val();
        const page_size = $("select[name=page_size]").val();
        const sorted_by = $("select[name=sort_by").val();

        fetch(`/my/get-referrals?level=${level}&page_size=${page_size}&sorted_by=${sorted_by}`).then(response => {
            if (response.status === 200){
                response.json().then(response => {
                    console.log(response);
                    renderRefs(response.referrals);
                    console.log(response.total_pages);
                    renderPagination(1, response.total_pages, 'loadPagination');
                    rememberFilters();
                    changePaginationCount(response.count);
                })
            }
        })
    });
    document.querySelector("select[name=page_size]").addEventListener("change", () => {
        const level = $("select[name=level]").val();
        const page_size = $("select[name=page_size]").val();
        const sorted_by = $("select[name=sort_by]").val();

        fetch(`/my/get-referrals?level=${level}&page_size=${page_size}&sorted_by=${sorted_by}`).then(response => {
            if (response.status === 200){
                response.json().then(response => {
                    console.log(response);
                    renderRefs(response.referrals);
                    console.log(response.total_pages);
                    renderPagination(1, response.total_pages, 'loadPagination');
                    rememberFilters();
                    changePaginationCount(response.count);
                })
            }
        })
    });

    document.querySelector("select[name=sort_by]").addEventListener("change", () => {
        const level = $("select[name=level]").val();
        const page_size = $("select[name=page_size]").val();
        const sorted_by = $("select[name=sort_by]").val();

        fetch(`/my/get-referrals?level=${level}&page_size=${page_size}&sorted_by=${sorted_by}`).then(response => {
            if (response.status === 200){
                response.json().then(response => {
                    console.log(response);
                    renderRefs(response.referrals);
                    console.log(response.total_pages);
                    renderPagination(1, response.total_pages, 'loadPagination');
                    rememberFilters();
                    changePaginationCount(response.count);
                })
            }
        })
    })
}


function getReferralPopup(referralId){
    fetch(`/get-referral-popup?user_id=${referralId}`).then(response => {
        if (response.status == 200){
            response.json().then(response => {
                document.querySelector(".ref-popup").innerHTML = response.content;
                openForm(document.querySelector(".ref-popup"));
            })
        }
    })
}

function closeRefPopup(){
    const popup = document.querySelector(".ref-popup");
    closeForm(popup);
}

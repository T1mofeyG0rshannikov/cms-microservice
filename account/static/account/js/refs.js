function renderRefs(refs){
    let refsHTML = '';
    for (let referral of refs){
        const refHTML = `
        <tr>
            <td class="ref">
                <div class="logo">
                    <img src="${ referral.profile_picture ? referral.profile_picture : '/static/account/images/nophoto.jpg' }" />
                </div>

                <p>${ referral.username } ${ referral.second_name ? referral.second_name : ""}</p>
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

function renderPagination(pageNum, totalPages){
    let pagination = `<a ${ pageNum == 1 ? 'class="active"' : "" } onclick="loadPagination(1)">1</a>`;

    if (pageNum > 4){
        pagination += `...`;
    }

    if (pageNum == 1){
        for (let num = 1; num <= totalPages; num++){
            if (pageNum < num && num < pageNum + 3){
                if (num != 1 && num != totalPages){
                    pagination += `<a ${ num == pageNum ? 'class="active"' : "" } onclick="loadPagination(${ num })">${ num }</a>`;
                }
            }
        }
    }

    else if (pageNum == totalPages){
        for (let num = 1; num <= totalPages; num++){
            if (pageNum-3 < num && num < pageNum){
                if (num != totalPages && num != 1){
                    pagination += `<a ${ num == pageNum ? 'class="active"' : "" } onclick="loadPagination(${ num }, ${totalPages})">${ num }</a>`;
                }
            }
        }
    }
    else{
        for (let num =1; num <= totalPages; num++){
            if (pageNum-2 < num && num < pageNum + 2){
                if (num != totalPages && num != 1){
                    pagination += `<a ${ num == pageNum ? 'class="active"' : "" } onclick="loadPagination(${ num }, ${totalPages})">${ num }</a>`;
                }
            }
        }
    }

    if (pageNum < totalPages - 3){
        pagination += `...`;
    }

    if (totalPages > 1){
        pagination += `<a ${ pageNum == totalPages ? 'class="active"' : "" } onclick="loadPagination(${ totalPages }, ${totalPages})">${ totalPages }</a>`;
    }

    if (totalPages > 1){
        document.querySelector(".pages").innerHTML = pagination;
    }
    else{
        document.querySelector(".pages").innerHTML = '';
    }
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
                renderPagination(pageNum, response.total_pages);
            })
        }
    })
}

function initRefsContent(){
    document.querySelector("select[name=level]").addEventListener("change", () => {
        const level = $("select[name=level]").val();
        const page_size = $("select[name=page_size]").val();
        const sorted_by = $("select[name=sort_by")

        fetch(`/my/get-referrals?level=${level}&page_size=${page_size}&sorted_by=${sorted_by}`).then(response => {
            if (response.status === 200){
                response.json().then(response => {
                    console.log(response);
                    renderRefs(response.referrals);
                    console.log(response.total_pages);
                    renderPagination(1, response.total_pages);
                })
            }
        })
    });
    document.querySelector("select[name=page_size]").addEventListener("change", () => {
        const level = $("select[name=level]").val();
        const page_size = $("select[name=page_size]").val();

        fetch(`/my/get-referrals?level=${level}&page_size=${page_size}`).then(response => {
            if (response.status === 200){
                response.json().then(response => {
                    console.log(response);
                    renderRefs(response.referrals);
                    console.log(response.total_pages);
                    renderPagination(1, response.total_pages);
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
                    renderPagination(1, response.total_pages);
                })
            }
        })
    })
}

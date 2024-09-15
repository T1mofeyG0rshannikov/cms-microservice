function getAlertIcon(alert){
    if (alert.status === "info"){
        return "/static/common/images/i.png";
    }

    return "/static/common/images/tick.png";
}


function addAlert(alert){
    const alertSpan = document.querySelector("span.indicator");

    alertSpan.style.width = "15px";
    alertSpan.style.height = "15px";

    const newAlertElem =
    `
    <div class="alert-elem">
        <div class="main">
            <img class="status" src="${getAlertIcon(alert)}" />

            <div class="alert-content">
                <a class="date">${ alert.date_created }</a>
                <a>${ alert.notification.message }</a>
            </div>
        </div>

        <img class="trash" data-id="${ alert.id }" src="/static/account/images/trash.png" />
    </div>
    `;

    const alertsContainer = document.querySelector(".alerts .content")
    alertsContainer.innerHTML += newAlertElem;
}

function deleteAlert(alert_id){
    const alertElems = document.querySelectorAll(".alerts .content .alert-elem");

    for (let alertElem of alertElems){
        if ($(alertElem.querySelector(".trash")).attr("data-id") == alert_id){
            alertElem.remove();
        }
    }

    fetch(`/notifications/delete/${alert_id}`);
}

let url = `ws://${window.location.hostname}/ws/socket-server/`

const notoficationsSocket = new WebSocket(url)

notoficationsSocket.onmessage = function(e){
    console.log('Data:', e.data.message)
    console.log('Data:', e.data)

    userAlert = JSON.parse(e.data).message
    console.log(userAlert)
    addAlert(userAlert);
}

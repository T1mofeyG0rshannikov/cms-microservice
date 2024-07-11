function addAlert(){
    const alertSpan = document.querySelector("span.indicator");

    console.log(alertSpan);
    alertSpan.style.width = "15px";
    alertSpan.style.height = "15px";
}

let url = `ws://localhost:8000/ws/socket-server/`

const notoficationsSocket = new WebSocket(url)

notoficationsSocket.onmessage = function(e){
    console.log('Data:', e.data)
    addAlert();
}

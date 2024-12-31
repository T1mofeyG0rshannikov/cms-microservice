function selectChat(chatId){
    fetch(`/get-chat?chat_id=${chatId}`).then(
        response => response.json()
    ).then(
        response => {
            const chatBody = document.querySelector(".chat-body")
            chatBody.innerHTML = response.content;
            document.querySelectorAll(".chat").forEach(chat => {
                chat.classList.remove("selected")
            })

            document.querySelectorAll(".chat").forEach(chat => {
                if ($(chat).attr("data-id") == chatId){
                    chat.classList.add("selected")
                }
            })

            messageTextarea = document.getElementById("message");
            messageTextarea.addEventListener("input", () => {
                if (messageTextarea.value !== ''){
                    document.querySelector(".chat-body button").disabled = false;
                }
                else{
                    document.querySelector(".chat-body button").disabled = true;
                }
            })

            saveChatInUrl(chatId);
        }
    )
}

const messangerBody = document.querySelector(".messanger-body");
const chatList = document.querySelector(".chat-list");

messangerBody.style.maxHeight = `calc(100vh - ${nav.getBoundingClientRect().height}px)`;
chatList.style.maxHeight = `calc(100vh - ${nav.getBoundingClientRect().height}px)`;
chatList.style.minHeight = `calc(100vh - ${nav.getBoundingClientRect().height}px)`;


function sendMessage(){
    let chatId = $(document.querySelectorAll(".chat.selected")).attr("data-id")
    fetch('/messanger/send-message', {
        method: "POST",
        body: JSON.stringify({
            'message_text': document.querySelector("#message").value,
            'chat_id': chatId
        })
    })
}


function saveChatInUrl(chatId){
    const url = new URL(window.location.href);
    url.searchParams.set('chat_id', chatId);
    window.history.replaceState(null, '', window.location.pathname + url.search);
}

let messageTextarea = document.getElementById("message");

messageTextarea.addEventListener("input", () => {
    if (messageTextarea.value !== ''){
        document.querySelector(".chat-body button").disabled = false;
    }
    else{
        document.querySelector(".chat-body button").disabled = true;
    }
})

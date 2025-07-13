function setTokens(access_token, refresh_token){
    localStorage.setItem("bankomag_access_token", access_token);
    localStorage.setItem("bankomag_refresh_token", refresh_token);
}

function getToken(){
    return localStorage.getItem("bankomag_access_token");
}

function getRefreshToken(){
    return localStorage.getItem("bankomag_refresh_token")
}

function deleteTokens(){
    localStorage.removeItem("bankomag_access_token");
    localStorage.removeItem("bankomag_refresh_token");
}

async function refreshTokensAPI(){
    const response = await fetch(`/user/refresh-tokens/${getRefreshToken()}`, {
        method: "POST"
    })

    return getData(response)
}
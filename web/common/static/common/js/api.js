async function getData(response){
    let data = null
    try{
        data = await response.json();
    }
    catch {

    }
    
    return {
      status: response.status,
      data: data,
    };
}

async function getUserAPI(domain){
    const token = getToken();

    const response = await fetch(`${window.location.protocol}//${domain}/user/get-user-info`, {
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': token
        }
    })

    return await getData(response)
}
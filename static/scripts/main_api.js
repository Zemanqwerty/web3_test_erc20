async function sendRegistrationData() {
    const username_text = document.getElementById("send_login");
    const password_text = document.getElementById("send_password");

    let username = username_text.value;
    let password = password_text.value;

    const response = await fetch("/api/registration", {
        "method": "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        "body": JSON.stringify({
            "username": username,
            "password": password
        })
    })

    const json = await response.json();
    console.log(JSON.stringify(json));

    console.log(json["status"])

    if (json["status"] == "success") {
        window.location.replace("/autz")
    }
    else{
        const alertText = document.getElementById('alertText')
        alertText.innerText = json["message"]
    }

    password_text.value = "";
    username_text.value = "";
}


async function sendAuthorizationData() {
    const username_text = document.getElementById("send_login");
    const password_text = document.getElementById("send_password");

    let username = username_text.value;
    let password = password_text.value;

    const response = await fetch("/api/authorization", {
        "method": "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        "body": JSON.stringify({
            "username": username,
            "password": password
        })
    })
    // then(res => (res.json()))
    //         .then(res => {
    //             return res;
    //         })

    const json = await response.json();
    
    if (json["status"] == "success") {
        window.location.replace("/")
    }
    else{
        const alertText = document.getElementById('alertText')
        alertText.innerText = json["message"]
    }

    password_text.value = "";
    username_text.value = "";
}


async function createNewProject() {
    const project_name = document.getElementById("project_name");
    const project_site = document.getElementById("project_site");
    const smart_contract = document.getElementById("smart_contract");
    const coin_count = document.getElementById("coin_count");
    const coin_price = document.getElementById("coin_price");

    let p_name = project_name.value;
    let p_site = project_site.value;
    let smrt_contract = smart_contract.value;
    let c_count = coin_count.value;
    let c_price = coin_price.value;

    const response = await fetch("/api/create_new_project", {
        "method": "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        "body": JSON.stringify({
            "project_name": p_name,
            "project_site": p_site,
            "smart_contract": smrt_contract,
            "coin_count": c_count,
            "coin_price": c_price,
        })
    })
    // then(res => (res.json()))
    //         .then(res => {
    //             return res;
    //         })

    const json = await response.json();
    
    if (json["status"] == "success") {
        window.location.replace("/")
    }
    else{
        const alertText = document.getElementById('alertText')
        alertText.innerText = json["message"]
    }
}





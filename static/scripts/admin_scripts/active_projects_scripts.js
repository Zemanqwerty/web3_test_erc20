document.onclick = function(event){
    event = event || window.event;
    if (!event.target) {
        event.target = event.srcElement;
    }
}

async function updateStatus () {
    const projectId = event.target.id
    console.log(event.target.className)

    const response = await fetch("/admin/to_finish", {
        "method": "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        "body": JSON.stringify({
            "id_project": projectId,
        })
    })

    const json = await response.json()

    if (json["status"] == "success") {
        console.log('success status update')
    }
}
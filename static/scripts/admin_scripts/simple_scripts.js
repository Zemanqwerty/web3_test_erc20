document.onclick = function(event){
    event = event || window.event;
    if (!event.target) {
        event.target = event.srcElement;
    }
}

async function updateStatus () {
    const projectId = event.target.id
    const projectStatus = event.target.className
    console.log(event.target.className)

    let project_status = 1

    if (projectStatus == "accept_button") {
        project_status = 2
    } else if (projectStatus == "reject_button") {
        project_status = 3
    };

    console.log(project_status);

    const response = await fetch("/admin/to_consider_project", {
        "method": "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        "body": JSON.stringify({
            "id_project": projectId,
            "project_status": project_status
        })
    });

    const json = await response.json();

    if (json["status"] == "success") {
        console.log('success status update');
        window.location.reload();
    }
}
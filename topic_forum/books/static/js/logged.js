
function logut_function() {
    $.ajax({
        type: "GET",
        headers: { 'X-CSRFToken': token },
        url: logout_url,
        success: (e) => {
            if (e['result'] == 'done') location.reload()
            else alert('Unable to perform action')
        }

    })
}
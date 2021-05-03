$('document').ready(function () {
    console.log('loading scripts')
    redundency()
    $('#DM_loading').hide()
})
function edit(pk) {
    $('#edit_new_text').val($('#' + pk + '_text').text())
    $('#edit_new_title').val($('#' + pk + '_title').text())
    $('#comment_edit_type').val('edit')
    $('#comment_edit_id').val(pk)
    $('#comment_edit_modal').modal('show')
}

function send_DM(pk, name) {
    let label = $('#DM_modal_title')
    if (!serialized_friend_list.includes(Number(pk))) {
        label.html(name + " (add to friends)");
        label.on('click', function () { add_friend(pk) })
    } else { label.html(name); label.css('color', 'green') }
    let modal = $('#DM_modal')
    modal.modal('show')
    $('#DM_modal_button').one('click', function () {
        $('#DM_loading').show()
        $.ajax({
            type: "POST",
            headers: { 'X-CSRFToken': token },
            url: DM_url,
            data: {
                "reciever_id": pk,
                "message_subject": $('#message_subject').val(),
                "message": $('#DM_message').val(),
            },
            success: (e) => {
                modal.modal('hide')
                if (e['result'] == 'error') { alert('ERROR') }
                else { alert('Message sent!') }
            },
            failure: () => { alert('server error'); modal.modal('hide') }
        })
    });
}
function redundency() {
    $('#DM_modal').on('hidden.bs.modal', function () {
        $('#DM_modal_button').off()
        let label = $('#DM_modal_title')
        label.off()
        label.css('color', 'black')
        $('#message_subject').val('')
        $('#DM_message').val('')
        $('#DM_loading').hide()
    })
}
function add_friend(pk) {
    $.ajax({
        type: 'POST',
        headers: { 'X-CSRFToken': token },
        url: friend_url,
        data: {
            'friend': pk
        },
        success: (e) => {
            if (e['result'] == 'error') alert('Unable to perform!')
            else $('#DM_modal_title').css('color', 'green')
        },
        failure: () => { alert('server error') }

    })
}
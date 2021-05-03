$('document').ready(function () {
    console.log('loading scripts')
    redundency()
    $('#DM_loading').hide()
    $('#edit_loading').hide()
})

function send_DM(pk, name) {
    let label = $('#DM_modal_title')
    if (!serialized_friend_list.includes(Number(pk))) {
        label.html(name + " (add to friends)");
        label.on('click', function () { add_friend(pk) })
    } else { label.html(name); label.css('color', 'green') }
    $('#DM_modal').modal('show')
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
                $('#DM_modal').modal('hide')
                if (e['result'] == 'error') { alert('ERROR') }
                else { alert('Message sent!') }
            },
            failure: () => { alert('server error') }
        })
    });
}
function edit_comment(pk) {
    let modal = $('#comment_edit_modal')
    modal.modal('show')
    let comment_text = $('#' + pk + '_text')
    let comment_title = $('#' + pk + '_title')
    let text = $('#edit_new_text')
    text.val(comment_text.html())
    let title = $('#edit_new_title')
    title.val(comment_title.html())
    $('#edit_comment_btn').one('click', function () {
        $('#edit_loading').show()
        $.ajax({
            type: "POST",
            headers: { 'X-CSRFToken': token },
            url: edit_url,
            data: {
                "type": false,
                "id": pk,
                "text": text.val(),
                "title": title.val(),
            },
            success: (e) => {
                modal.modal('hide')
                if (e['result'] == 'error') { alert('ERROR') }
                else { comment_text.html(text.val()); comment_title.html(title.val()) }
            },
            failure: () => { modal.modal('hide'); alert('server error') }
        })
    });
}
function redundency() {
    $('#DM_modal').on('hidden.bs.modal', function () {
        $('#DM_modal_button').off()
        let label = $('#DM_modal_title')
        label.off()
        label.css('color', 'black')
        $('#DM_loading').hide()
    })
    $('#comment_edit_modal').on('hidden.bs.modal', function () {
        $('#edit_comment_btn').off()
        $('#edit_loading').hide()
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
function delete_friend(pk, inst) {
    $.ajax({
        type: 'POST',
        headers: { 'X-CSRFToken': token },
        url: friend_url,
        data: {
            'delete': 'delete',
            'friend': pk
        },
        success: (e) => { $('#' + inst).remove() },
        failure: () => { alert('server error') }
    })
}
function edit_DM(pk, action, agent) {
    $.ajax(
        {
            type: 'POST',
            headers: { 'X-CSRFToken': token },
            url: DM_url,
            data: {
                'type': action,
                'by': agent,
                'id': pk
            },
            success: (e) => { console.log(e) },
            failure: () => { console.log('server error') }
        }
    )
}
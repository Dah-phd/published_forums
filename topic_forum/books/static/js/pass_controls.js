$('document').ready(function () {
    $('#log_loading').hide();
    console.log('loading scripts');
    modaled_login();
    restore_login_modal();
    new_pass();
    restore_reset_modal()
})
function modaled_login() {
    $('#login_modal_button').on('click', function () {
        $('#log_loading').show();
        let label = $('#login_modal_title');
        $.ajax({
            type: "POST",
            headers: { 'X-CSRFToken': token },
            url: login_url,
            data: {
                'username': $('#id_username').val(),
                'password': $('#id_password').val()
            },
            success: (e) => {
                if (e['result'] == 'failed') { label.css('color', 'red'); label.html('User not found!') }
                else { location.reload() }
            }
        })
    });
}
function restore_login_modal() {
    $('#login_modal').on('hidden.bs.modal', function () {
        let label = $('#login_modal_title');
        $('#log_loading').hide();
        label.css('color', 'black');
        label.html('Login:');
        $('#id_username').val('');
        $('#id_password').val('');
    })
}
function new_pass() {
    $('#reset_modal_button').on('click', function () {
        $('#loading').show();
        $.ajax({
            type: "POST",
            headers: { 'X-CSRFToken': token },
            url: reset_url,
            data: {
                "email": $('#id_email').val()
            },
            success: (e) => {
                $('#reset_modal').modal('hide'); alert('You will recieve an email with instructions, shortly.')
            },
            failure: () => { alert('failure'); },
        });
    });
}
function restore_reset_modal() {
    $('#loading').hide();
    $('#login_modal').on('hidden.bs.modal', function () {
        $('#id_email').val('');
        $('#loading').hide();
    })
}
function init_reset() {
    $('#login_modal').modal('hide');
    $('#reset_modal').modal('show');
}

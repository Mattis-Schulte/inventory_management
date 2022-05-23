loadAjaxContent = function(page) {
    $.ajax({
        url: '../' + page + '/',
        async: true,
        success: function(data) {
            $('#page-content').html(data);
            $('#load-content-error').hide();
            window.history.pushState(null, null, '../' + page + '/');
            $('#customID').remove();
            },
        error: function() {
            loadContentError();
            window.history.pushState(null, null, '../' + page + '/');
            },
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
}

loadContentError = function() {
    document.title = "Fehler – SZUT Inventur Management"
    $('#load-content-error').show();
    $('#page-content').html('');
}

$(document).ready(function() {
  $("#login_form").on('submit', function(e){
     e.preventDefault();
        var form = $(this);
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data) {
                alert(data);
            },
            error: function(data) {
                alert(data);
            },
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
  });
});
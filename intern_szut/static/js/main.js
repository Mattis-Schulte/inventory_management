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
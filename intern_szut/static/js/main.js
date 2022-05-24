var current_highlight;

$(document).ready(function() {
  $("#login-form").on('submit', function(e){
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

loadAjaxContent = function(page) {
    $.ajax({
        url: '/' + page + '/',
        async: true,
        success: function(data) {
            $('#custom-css').remove();
            $('#page-content').html(data);
            $('#load-content-error').hide();
            window.history.pushState(null, null, '/' + page + '/');
            setHighlight(page);
            },
        error: function() {
            $('#custom-css').remove();
            loadContentError();
            window.history.pushState(null, null, '/' + page + '/');
            setHighlight(page);
            },
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
}

loadContentError = function() {
    document.title = "Fehler – SZUT Inventur Management";
    $('#load-content-error').show();
    $('#page-content').html('');
}

setHighlight = function(to_highlight) {
    $('#' + to_highlight).addClass('highlight');
    if (current_highlight && current_highlight !== to_highlight) {
        $('#' + current_highlight).removeClass('highlight');
    }
    current_highlight = to_highlight;
}
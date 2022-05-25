var current_highlight;

$(document).ready(function() {
  $('#login-form').on('submit', function(e){
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

  $('.menu-button-wrapper').click(function() {
      $('.account-card').hide();
      $('.top-bar-login').attr('aria-pressed', 'false');
      $('.top-bar-login i').removeClass('bi-chevron-up');

      $('.menu-button-wrapper').attr('aria-pressed', function(i, attr) {
            return attr == 'true' ? 'false' : 'true';
      });
      $('.nav-side-bar').toggleClass('nav-side-bar-open');
  });

  $('.top-bar-login').click(function() {
      $('.nav-side-bar').removeClass('nav-side-bar-open');
      $('.menu-button-wrapper').attr('aria-pressed', 'false');

      $('.account-card').toggle();
      $('.top-bar-login i').toggleClass('bi-chevron-up');
      $('.top-bar-login').attr('aria-pressed', function(i, attr) {
            return attr == 'true' ? 'false' : 'true';
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
            $('.nav-side-bar').removeClass('nav-side-bar-open');
            window.history.pushState(null, null, '/' + page + '/');
            setHighlight(page);
            },
        error: function() {
            $('#custom-css').remove();
            loadContentError();
            $('.nav-side-bar').removeClass('nav-side-bar-open');
            window.history.pushState(null, null, '/' + page + '/');
            setHighlight(page);
            },
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
}

loadContentError = function() {
    document.title = 'Fehler – SZUT Inventur Management';
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
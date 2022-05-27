var current_highlight;

$(document).ready(function() {
  $('#login-form').on('submit', function(e){
     e.preventDefault();
      let form = $(this);
      $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            cache: "false",
            beforeSend: function() {
                $('.login-button img').hide();
                $('.login-button p').hide();
                $('.loader-wrapper').css('display', 'flex');
                $('.login-form :input:not([type=hidden])').prop('disabled', true);
            },
            complete: function() {
                $('.login-button img').show();
                $('.login-button p').show();
                $('.loader-wrapper').css('display', 'none');
                $('.login-form :input:not([type=hidden])').prop('disabled', false);
            },
            success: function(data) {
                // alert(data); // Debug
                if (data.startsWith('Success')) {
                    $('.account-card').hide();
                    $('.top-bar-account-link').attr('aria-pressed', 'false');
                    $('.top-bar-account-link i').removeClass('bi-chevron-up');
                    $('.on-login-error').hide();
                } else if (data.includes('{"ErrorCode":"InvalidUser"}')) {
                    $('.on-login-error').text('Benutzername oder Passwort falsch').show();
                } else {
                    $('.on-login-error').text('Ein Fehler ist aufgetreten').show();
                }
            },
            error: function() {
                $('.on-login-error').text('Ein Fehler ist aufgetreten').show();
            },
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },

        });
  });

  $('.menu-button-wrapper, .nav-side-bar-overlay').click(function() {
      $('.account-card').hide();
      $('.top-bar-account-link').attr('aria-pressed', 'false');
      $('.top-bar-account-link i').removeClass('bi-chevron-up');

      $('.menu-button-wrapper').attr('aria-pressed', function(i, attr) {
            return attr === 'true' ? 'false' : 'true';
      });
      $('.nav-side-bar').toggleClass('nav-side-bar-open');
  });

  $('.top-bar-account-link').click(function() {
      $('.nav-side-bar').removeClass('nav-side-bar-open');
      $('.menu-button-wrapper').attr('aria-pressed', 'false');

      $('.account-card').toggle();
      $('.top-bar-account-link i').toggleClass('bi-chevron-up');
      $('.top-bar-account-link').attr('aria-pressed', function(i, attr) {
            return attr === 'true' ? 'false' : 'true';
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
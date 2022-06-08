var current_highlight;

$(document).ready(function() {
  $('#login-form').on('submit', function(e){
      e.preventDefault();
      let form = $(this);
      $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            cache: false,
            beforeSend: function() {
                $('.login-button img').hide();
                $('.login-button p').hide();
                $('.login-loader-wrapper').css('display', 'flex');
                $('.login-form :input:not([type=hidden])').prop('disabled', true);
            },
            complete: function() {
                $('.login-button img').show();
                $('.login-button p').show();
                $('.login-loader-wrapper').css('display', 'none');
                $('.login-form :input:not([type=hidden])').prop('disabled', false);
            },
            success: function(data) {
                // alert(data); // Debug
                if (data.startsWith('Success')) {
                    location.reload();
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

  $('#search-form').on('keyup change submit', function(e){
      let form = $(this);
      makeSearch(e, form);
  });

  $('#sidebar-search-form').on('submit', function(e){
      let form = $(this);
      makeSearch(e, form);
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

  $('.top-bar-account-link, .account-li-not-logged-in').click(function() {
      $('.nav-side-bar').removeClass('nav-side-bar-open');
      $('.menu-button-wrapper').attr('aria-pressed', 'false');

      $('.account-card').toggle();
      $('.top-bar-account-link i').toggleClass('bi-chevron-up');
      $('.top-bar-account-link').attr('aria-pressed', function(i, attr) {
            return attr === 'true' ? 'false' : 'true';
      });
  });
});

loadAjaxContent = function(page, push_state=true, clear_search=true) {
    $.ajax({
        url: page,
        cache: false,
        success: function(data) {
            $('#custom-css').remove();
            $('#page-content').html(data);
            $('#load-content-error').hide();
            $('.nav-side-bar').removeClass('nav-side-bar-open');
            $('.menu-button-wrapper').attr('aria-pressed', 'false');
            $('.account-card').hide();
            $('.top-bar-account-link').attr('aria-pressed', 'false');
            $('.top-bar-account-link i').removeClass('bi-chevron-up');
            if (push_state) {
                window.history.pushState(null, null, page);
            }
            setHighlight(page.split('/')[1]);
            $('.main-content-wrapper').animate({scrollTop: 0}, 0);
            if (clear_search) {
                $('#search-form').find('input').val('');
            }
        },
        error: function() {
            $('#custom-css').remove();
            loadContentError();
            $('.nav-side-bar').removeClass('nav-side-bar-open');
            $('.menu-button-wrapper').attr('aria-pressed', 'false');
            $('.account-card').hide();
            $('.top-bar-account-link').attr('aria-pressed', 'false');
            $('.top-bar-account-link i').removeClass('bi-chevron-up');
            if (push_state) {
                window.history.pushState(null, null, page);
            }
            setHighlight(page.split('/')[1]);
        },
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
}

$(window).bind("popstate", function () {
  loadAjaxContent(location.pathname + location.search, false);
});

logout = function(url) {
    $.ajax({
        url: url,
        cache: false,
        success: function() {
            location.reload();
        },
        error: function() {
            $('#custom-css').remove();
            loadContentError();
            $('.account-card').hide();
            $('.top-bar-account-link').attr('aria-pressed', 'false');
            $('.top-bar-account-link i').removeClass('bi-chevron-up');
        },
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
}

function loadContentError() {
    document.title = 'Fehler – SZUT Inventur Management';
    $('#load-content-error').show();
    $('#page-content').html('');
}

function setHighlight(to_highlight) {
    $('#' + to_highlight).addClass('highlight');
    if (current_highlight !== to_highlight) {
        $('#' + current_highlight).removeClass('highlight');
    }
    current_highlight = to_highlight;
}

function makeSearch(e, form) {
    e.preventDefault();
    let search_base_url = form.attr('action');
    let search_value = form.find('input').val();
    if (search_value.length > 0) {
        var search_url = search_base_url + '?q=' + search_value;
        if (e.type !== 'submit' || e.keyCode !== 13) {
            loadAjaxContent(search_url, false, false);
        }
    } else {
        loadAjaxContent('/overview/', true);
    }

    if (e.type === 'submit' || e.keyCode === 13 || e.type === 'change') {
        document.activeElement.blur();
        form.find('input').blur();
        loadAjaxContent(search_url, true, false);
    }
}

function fetchFilter() {
    let filter_values = [];
    $('.filter-box-item').each(function() {
        var filter_value = $(this).find('select').val();
        let filter_id = $(this).find('select').attr('id');
        filter_values.push({
            'id': filter_id,
            'value': filter_value
        });
    });
    return filter_values;
}

function applyFilter() {
    let filter_values = fetchFilter();

    let filter_url = location.pathname;
    let number_of_filters = filter_values.length - filter_values.filter(function(item) { return item.value === 'all' }).length;

    if (number_of_filters > 0) {
        filter_url += '?';
        for (let i = 0; i < filter_values.length; i++) {
            if (filter_values[i].value !== 'all') {
                filter_url += filter_values[i].id + '=' + filter_values[i].value + '&';
            }
        }
        filter_url = filter_url.substring(0, filter_url.length - 1);
    }

    loadAjaxContent(filter_url);
}
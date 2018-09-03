$(document).ready(function() {
  const getCookie = (name) => {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          let cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = jQuery.trim(cookies[i]);
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  };
  const csrftoken = getCookie('csrftoken');

  const csrfSafeMethod = (method) => {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  };

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  $('.tape-dialog-btn').on('click', function() {
    const commentParent = $(this).parent();
    const commentContent = commentParent.find('textarea');
    $(this).attr('disabled', 'disabled');

    if (commentContent.val()) {
      $.post('send-comment/',
        {'post_id': commentContent.attr('data-post-id')[0], 'comment': commentContent.val()}, function (data) {
          commentParent.find('.tape-dialog-all').before(
            '<div class="tape-dialog-wrapp"><img src="' + data.author_profile_image + '" alt="">\n' +
            '<div class="tape-dialog-content">\n' +
            '<div class="tape-dialog-header">\n' +
            '<p>' + data.author_full_name + '</p><span>' + data.date_time + '</span>\n' +
            '</div><span>' + commentContent.val() + '</span>\n' +
            '</div>\n' +
            '</div>');
            $(this).attr('disabled', 'enabled');
            commentContent.val('');
      });
    }
  })
});
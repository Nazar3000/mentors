$(document).ready(function() {
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
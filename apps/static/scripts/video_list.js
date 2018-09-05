$(document).ready(function() {
  $('.with-font').on('click', function() {
    const parentNode = $(this).parent().parent();
    if (parentNode.find('.video-all-btn').length) {
      parentNode.find('.video-all-btn').text('Переглянути ще раз');
      parentNode.find('.video-all-btn').attr('class', 'video-init-all-btn');
    } else if (parentNode.find('.video-init-all-btn').length) {
      parentNode.find('.video-init-all-btn').text('Переглянути');
      parentNode.find('.video-init-all-btn').attr('class', 'video-all-btn');
    }

    $.post('', {'video_id': $(this).attr('data-id')});
  })
});
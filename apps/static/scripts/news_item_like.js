$('.like-block').on('click', function(e) {
  e.preventDefault();

  const postId = $(this).attr('data-id');
  const likeLink = $(this).find('a');
  $.post('/mentor/posts/like-post/', {'post_id': postId}, function (data) {
    likeLink.text(`(${data.likes})`);
  })
});
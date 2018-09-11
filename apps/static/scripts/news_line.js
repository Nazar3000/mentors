const meetingList = new Vue({
  el: '#news-line',
  delimiters: ['[[', ']]'],
  data: {
    addNews: false,
    newPostData: {
      text: '',
      image: '',
    },
    posts: []
  },
  created() {
    $.get('?get_posts', (data) => {
      this.posts = data;
    })
  },
  methods: {
    addPostImage(event) {
      this.newPostData.image = event.target.files[0];
    },
    getPostImageUrl(image) {
      return URL.createObjectURL(this.newPostData.image);
    },
    sendNewPost() {
      const formData = new FormData();
      formData.append('text', this.newPostData.text);
      formData.append('image', this.newPostData.image);
      formData.append('new_post', '');

      $.ajax({
        url: '',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
        type: 'POST',
        success: (data) => {
          this.posts = [...data, ...this.posts];
          this.addNews = false;
          this.newPostData = {
            text: '',
            image: '',
          }
        }
      });
    }
  }
});

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
const meetingList = new Vue({
  el: '#news-line',
  delimiters: ['[[', ']]'],
  data: {
    addNews: false,
    newPostData: {
      text: '',
      image: '',
    },
    posts: [],
    newComments: [],
    modes: {
      view: 0,
      edit: 1
    }
  },
  created() {
    $.get('?get_posts', (data) => {
      this.posts = data;
      this.posts.map(p => {
        p.mode = this.modes.view;
        return p;
      });
    });
    if (window.location.search.substring(1).includes('addPost')) {
      this.addNews = true;
    }
  },
  methods: {
    addPostImage(event) {
      this.newPostData.image = event.target.files[0];
    },
    getPostImageUrl(image) {
      return URL.createObjectURL(this.newPostData.image);
    },
    likePost(postId) {
      $.post('/mentor/posts/like-post/', {'post_id': postId}, (data) => {
        this.posts.find(p => p.id === postId).likes = data.likes;
      })
    },
    addNewComment(value, postId) {
      if (this.newComments.find(c => c.postId === postId)) {
        this.newComments.find(c => c.postId === postId).content = value;
      } else {
        this.newComments.push({ postId: postId, content: value });
      }
    },
    sendNewComment(postId) {
      const posts = this.posts;
      const comment = this.newComments.find(c => c.postId === postId).content;
      $.post('send-comment/',
        {'post_id': postId, 'comment': comment}, function (data) {

        posts.find(p => p.id === postId).comments.push(data);
      });
    },
    deletePost(postId) {
      const posts = this.posts;
      $.post('', {'delete': true, 'post_id': postId}, function () {
        const index = posts.indexOf(posts.find(p => p.id === postId));
        posts.splice(index, 1);
      });
    },
    changePostMode(postId, mode) {
      const post = this.posts.find(p => p.id === postId);
      post.mode = mode;
      const index = this.posts.indexOf(post);
      this.posts.splice(index, 1);
      this.posts.splice(index, 0, post)
    },
    changePost(post) {
      const formData = new FormData();
      const currPost = post ? post : this.newPostData;
      formData.append('content', currPost.text);
      formData.append('image', currPost.image);
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
          console.log(data);
          if (post && post.hasOwnProperty('id')) {
            this.posts.splice(this.posts.indexOf(post), 0, data);
            this.changePostMode(data.id, this.modes.view);
          } else {
            this.posts.unshift(data);
            this.newPostData = {
              text: '',
              image: '',
            };
            this.addNews = false;
          }
        }
      });
    }
  }
});

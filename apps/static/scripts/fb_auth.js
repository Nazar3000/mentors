const sendFbData = new Vue({
  el: '#fb-signup',
  delimiters: ['[[', ']]'],
  data: {
    userData: {
      first_name: '',
      last_name: '',
      email: ''
    }
  },
  methods: {
    fetchFbData() {
      FB.login(res => {
        if (res.authResponse) {
          FB.api('/me?fields=first_name,last_name,email', response => {
            this.userData = response;
          });
        }
      });
    }
  }
});
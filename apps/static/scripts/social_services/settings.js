new Vue({
  el: '#social-service-edit',
  delimiters: ['[[', ']]'],
  data: {
    service: {
      'name' : '',
      'city' : '',
      'address' : '',
      'phone_numbers' : '',
      'profile_image' : '',
      'email': '',

      'password_old': '',
      'password_new1': '',
      'password_new2': '',
    },
    errors: {}
  },
  created() {
    $.get('?get_mentor_data', (res) => {
      this.service = Object.assign(this.service, res);
    });
  },
  methods: {
    updateService() {
      $.post('', this.service, (res) => {
        if (res.hasOwnProperty('status') && res.status === 'success') {
          window.location.href = "/social-service/main/";
        } else {
          this.errors = res;
        }
      })
    }
  }
});
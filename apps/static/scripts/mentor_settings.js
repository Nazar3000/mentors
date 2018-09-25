const mentorEdit = new Vue({
  el: '#mentor-edit',
  delimiters: ['[[', ']]'],
  data: {
    mentor: {
      'first_name': '',
      'last_name': '',
      'date_of_birth': '',
      'phone_number': '',
      'email': '',
      'actual_address': '',

      'password_old': '',
      'password_new1': '',
      'password_new2': '',
    },
    errors: {}
  },
  created() {
    $.get('?get_mentor_data', (res) => {
      this.mentor = Object.assign(this.mentor, res);
    });
  },
  methods: {
    updateMentor() {
      $.post('', this.mentor, (res) => {
        if (res.hasOwnProperty('status') && res.status === 'success') {
          window.location.href = "/mentor/office/";
        } else {
          this.errors = res;
        }
      })
    }
  }
});
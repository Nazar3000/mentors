new Vue({
  el: '#social-service-edit',
  delimiters: ['[[', ']]'],
  data: {
    service: {
      'name' : '',
      'city' : '',
      'address' : '',
      'phone_numbers' : '',
      'profile_image' : '/static/img/empty-img.png',
      'email': '',

      'password_old': '',
      'password_new1': '',
      'password_new2': '',
    },
    default_profile_image: '/static/img/empty-img.png',
    errors: {}
  },
  created() {
    $.get('?get_mentor_data', (res) => {
      this.service = Object.assign(this.service, res);
    });
  },
  methods: {
    updateService() {
      let formData = new FormData();
      for (let key in this.service) {
          if (this.service.hasOwnProperty(key)) {
              formData.append(key, this.service[key]);
          }
      }

      $.ajax({
        url: '',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
        type: 'POST',
        success: (res) => {
          if (res.hasOwnProperty('status') && res.status === 'success') {
            window.location.href = "/social-service/main/";
          } else {
            this.errors = res;
          }
        }
      });
    },
    getImageUrl(img) {
      if (img) {
        return typeof img === 'string' ? img : URL.createObjectURL(img);
      }
    },
    changeProfileImage(event) {
      this.service.profile_image = event.target.files[0];
    },
    deleteProfileImage() {
      this.service.profile_image = this.default_profile_image;
    },
  }
});
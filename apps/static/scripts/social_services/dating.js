const vm = new Vue({
  el: '#dating-form',
  delimiters: ['[[', ']]'],
  data: {
    searchValue: '',
    selectedSocialService: {},
    baseSocialService: {},
    searchedSocialServices: [],
    coordinator: {
      full_name: '',
      phone_numbers: '',
      email: ''
    },
    modalView: false,
    errors: {
      modal: {}
    }
  },
  methods: {
    submitForm() {
      const formData = new FormData();
      const mergedObj = {...this.selectedSocialService, ...this.coordinator};
      if (typeof this.selectedSocialService.phone_numbers === 'string') {
        mergedObj.phone_numbers = this.selectedSocialService.phone_numbers.split(',');
      } else {
        mergedObj.phone_numbers = this.selectedSocialService.phone_numbers;
      }
      if (this.coordinator.phone_numbers) {
        mergedObj.coordinator_phone_numbers = this.coordinator.phone_numbers.split(',');
      }
      for (let key in mergedObj) {
          if (mergedObj.hasOwnProperty(key)) {
              formData.append(key, mergedObj[key]);
          }
      }

      $.ajax({
        url: '/social-service/dating/',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
        type: 'POST',
        success: (res) => {
          if (res.status === 'success') {
            window.location.replace('/social-service/main/');
          } else {
            this.errors = res;
          }
        }
      });
    },
    submitModal() {
      const formData = new FormData();
      const data = this.baseSocialService;
      data['name'] = data.city + ', ' + data.address;

      for (let key in this.baseSocialService) {
          if (this.baseSocialService.hasOwnProperty(key)) {
              formData.append(key, this.baseSocialService[key]);
          }
      }

      $.ajax({
        url: '/social-service/dating/?add_new_base_service',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
        type: 'POST',
        success: (res) => {
          if (res.pk) {
            this.selectedSocialService = this.baseSocialService;
            this.selectedSocialService.pk = res.pk;
            this.modalView = false;
          } else {
            this.errors = {'modal': res};
          }
        }
      });
    }
  },
  watch: {
    searchValue: function (newVal) {
      if (newVal) {
        $.get(`/social-service/dating/?search_value=${newVal}&filter=unlinked`, (res) => {
          this.searchedSocialServices = res;
        });
      } else {
        this.searchedSocialServices = [];
      }
    }
  }
});
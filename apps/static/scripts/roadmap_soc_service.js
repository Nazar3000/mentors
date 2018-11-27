const careerList = new Vue({
  el: '#soc-service-block',
  delimiters: ['[[', ']]'],
  data: {
    searchValue: '',
    selectedSocialService: {},
    searchedSocialServices: []
  },
  created() {
  },
  methods: {
  },
  watch: {
    searchValue: function (newVal) {
      if (newVal) {
        $.get(`/social-service/dating/?search_value=${newVal}`, (res) => {
          this.searchedSocialServices = res;
        });
      } else {
        this.searchedSocialServices = [];
      }
    },
    selectedSocialService: function (newVal) {
      const formData = new FormData();
      formData.append('base_soc_service_center_id', newVal['pk']);

      $.ajax({
        url: '/mentor/roadmap/step1/?add_base_social_service',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
        type: 'POST'
      });
    }
  }
});
new Vue({
  el: '#social-service-center-table',
  delimiters: ['[[', ']]'],
  data: {
    social_services: []
  },
  created() {
    $.get('?social_service_grade', (res) => {
      this.social_services = res;
    })
  },
  methods: {
  },
});
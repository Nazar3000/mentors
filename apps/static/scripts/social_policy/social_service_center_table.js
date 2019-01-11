new Vue({
  el: '#social-service-center-table',
  delimiters: ['[[', ']]'],
  data: {
    social_services: [],
    sliceSize: 3
  },
  created() {
    $.get('?social_service_grade', (res) => {
      this.social_services = res;
    })
  },
  methods: {
    changeSliceSize() {
      this.sliceSize = this.sliceSize === 3 ? this.social_services.length : 3;
    },
  },
});
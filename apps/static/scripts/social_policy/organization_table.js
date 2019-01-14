new Vue({
  el: '#organization-table',
  delimiters: ['[[', ']]'],
  data: {
    social_services: [],
    sliceSize: 3
  },
  created() {
    $.get('?organization_grade', (res) => {
      this.social_services = res;
    })
  },
  methods: {
    changeSliceSize() {
      this.sliceSize = this.sliceSize === 3 ? this.social_services.length : 3;
    },
  },
});
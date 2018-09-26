const reportSsc = new Vue({
  el: '#prefooter-report',
  delimiters: ['[[', ']]'],
  data: {
    selected_ssc: null,
    content: ''
  },
  methods: {
    selectSsc(sccId) {
      this.selected_ssc = sccId;
    },
    submitReport() {
      $.post('/mentor/prefooter/report-ssc/', this.$data, () => {
        $('.complaint-modal').fadeOut(400);
      })
    }
  }
});

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

const sscAssessment = new Vue({
  el: '#prefooter-assess',
  delimiters: ['[[', ']]'],
  data: {
    grade: null,
    mentor_help_description: '',
    mentor_pair_help_description: '',
  },
  methods: {
    setGrade(grade) {
      this.grade = grade;
    },
    submitAssessment() {
      $.post('/mentor/prefooter/assess-ssc/', this.$data, () => {
        $('.rate-place-modal').fadeOut(400);
      })
    }
  }
});

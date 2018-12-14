new Vue({
  el: '#footer',
  delimiters: ['[[', ']]'],
  data: {
    content: '',
    modalOpened: false
  },
  methods: {
    submitImprovement() {
      $.post('/offer-improvement/', {'content': this.content}, () => {
        this.modalOpened = false;
      })
    }
  }
});
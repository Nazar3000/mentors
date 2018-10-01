const careerList = new Vue({
  el: '#career-list',
  delimiters: ['[[', ']]'],
  data: {
    proforientations: [[]],
    selected_proforientation: {},
    agreed: false,
    userId: ''
  },
  created() {
    $.get('?get_careers', (res) => {
      this.proforientations = res;
    })
  },
  methods: {
    selectProforientation(proforientation) {
      this.selected_proforientation = proforientation;
      if (this.selected_proforientation.related_mentors.includes(userId)) {
        this.agreed = true;
      }
      $('.career-modal').fadeIn(500);
    },
    unselectProforientation() {
      this.selected_proforientation = {};
      $('.career-modal').fadeOut(400);
    },
    submitRelation() {
      if (this.agreed && !(this.selected_proforientation.related_mentors.includes(userId))) {
        this.selected_proforientation.related_mentors.push(userId);
        console.log(this.proforientations, this.selected_proforientation.id);
        this.proforientations.find(
          p => p.id === this.selected_proforientation.id).related_mentors.push(userId);
      } else if (!this.agreed && this.selected_proforientation.related_mentors.includes(userId)) {
        const relatedId = this.proforientations.find(
          p => p.id === this.selected_proforientation.id).related_mentors.indexOf(userId);
        this.proforientations.find(
          p => p.id === this.selected_proforientation.id).related_mentors.splice(relatedId, 1);
      }
      console.log(this.proforientations.find(
        p => p.id === this.selected_proforientation.id));
      this.unselectProforientation();
    }
  }
});
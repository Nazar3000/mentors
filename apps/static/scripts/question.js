new Vue({
  el: '#question',
  delimiters: ['[[', ']]'],
  data: {
    questions: [],
    searchedQuestions: [],
    searchString: ''
  },
  created() {
      $.get('?get_common_questions', (res) => {
        this.questions = res;
        this.searchedQuestions = this.questions;
      })
  },
  watch: {
    searchString: function (newSearchString) {
      const searchableFields = ['title'];
      this.searchedQuestions = this.questions.filter(m => {
        let searched = false;

        for (let field of searchableFields) {
          if (m[field] && !searched) {
            searched = m[field].toLowerCase().includes(newSearchString.toLowerCase());
          }
        }
        return searched;
      });
    },
  }
});
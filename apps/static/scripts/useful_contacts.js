new Vue({
  el: '#contacts',
  delimiters: ['[[', ']]'],
  data: {
    contacts: [],
    searchedContacts: [],
    searchString: '',
    activePage: 1
  },
  created() {
    $.get('?get_contacts', (res) => {
      this.contacts = res;
    })
  },
  methods: {
  },
  watch: {
    searchString: function (newSearchString) {
      const contacts = this.contacts;
      const searchableFields = ['name', 'email', 'address'];
      const preSearchedContacts = [].concat.apply([], contacts);

      this.searchedContacts = preSearchedContacts.filter(m => {
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
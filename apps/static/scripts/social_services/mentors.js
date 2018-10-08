const mentors = new Vue({
  el: '#mentors',
  delimiters: ['[[', ']]'],
  data: {
    lightMentors: [],
    mentorStatuses: {},
    publicServices: [],
    expanded: false,
    extendedMentor: {}
  },
  created() {
    this.getLightData();
  },
  methods: {
    getLightData() {
      $.get('?get_light_data', (res) => {
        this.lightMentors = res.mentors_data;
        this.mentorStatuses = res.mentor_statuses;
        this.publicServices = res.public_services;
      })
    },
    getExtendedMentorData() {
      this.expanded = !this.expanded;

      if (this.expanded) {
        $.get(`?get_extended_data&soc_service_id=${soc_service_id}`, (res) => {
          this.extendedMentor = res;
        });
      }
    }
  }
});
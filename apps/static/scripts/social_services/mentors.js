const mentors = new Vue({
  el: '#mentors',
  delimiters: ['[[', ']]'],
  data: {
    lightMentors: [],
    mentorStatuses: {},
    publicServices: [],
    expanded: false,
    extendedMentor: {},
    mentorSocServiceData: {},
    socServiceId: soc_service_id
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
          this.extendedMentor = res.mentor_data;
          this.mentorSocServiceData = res.mentor_social_service_center_data;
        });
      }
    }
  },
  watch: {
    lightMentors: {
      handler: function (oldVal, newVal) {
        if (newVal.length) {
          $.ajax({
            url: '',
            dataType: 'json',
            data: JSON.stringify({change_light_data: newVal}),
            contentType: 'application/json',
            type: 'POST',
            success: (res) => {
              console.log(res);
            }
          });
        }
      },
      deep: true
    }
  }
});
const mentors = new Vue({
  el: '#mentors',
  delimiters: ['[[', ']]'],
  data: {
    lightMentors: [],
    mentorStatuses: {},
    publicServices: [],
    expanded: false,
    mentorCardView: true,
    mentorSocServeDataView: true,
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
    },
    submitMentorCard() {
      $.ajax({
        url: '',
        dataType: 'json',
        data: JSON.stringify({change_extended_data: this.extendedMentor}),
        contentType: 'application/json',
        type: 'POST',
        success: (res) => {
          if (res.status === 'success') {
            this.mentorCardView = true;
          } else {
            console.log(res);
          }
        }
      });
    },
    submitMentorSocServeData() {
      $.ajax({
        url: '',
        dataType: 'json',
        data: JSON.stringify({change_social_service_center_data: this.mentorSocServiceData}),
        contentType: 'application/json',
        type: 'POST',
        success: (res) => {
          if (res.status === 'success') {
            this.mentorSocServeDataView = true;
          } else {
            console.log(res);
          }
        }
      });
    },
    getDateFromString(dateString) {
      const dateInts = dateString.split('.');
      return new Date(parseInt(dateInts[2]), parseInt(dateInts[1]) - 1, parseInt(dateInts[0]));
    },
    getDateFormatted(dateString) {
      if (dateString) {
        const date = this.getDateFromString(dateString);
        const options = {year: 'numeric', month: 'long', day: 'numeric'};
        return date.toLocaleDateString('uk-UK', options);
      } else {
        return '';
      }
    },
    getAge(dateString) {
      if (dateString) {
        dateString = dateString.split('.');
        const today = new Date();
        const year = today.getFullYear();
        const month = today.getMonth() + 1;
        const day = today.getDate();
        const yy = parseInt(dateString[2]);
        const mm = parseInt(dateString[1]);
        const dd = parseInt(dateString[0]);
        let years = 0, months = 0;

        years = year - yy;
        if (month * 100 + day < mm * 100 + dd) {
          years = years - 1;
          months = months + 12;
        }
        return years;
      } else {
        return 0;
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
            type: 'POST'
          });
        }
      },
      deep: true
    }
  }
});
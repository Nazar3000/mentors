const mentors = new Vue({
  el: '#mentors',
  delimiters: ['[[', ']]'],
  data: {
    lightMentors: [],
    searchedMentors: [],
    mentorStatuses: {},
    publicServices: [],
    expanded: false,
    mentorCardView: true,
    mentorSocServeDataView: true,
    extendedMentor: {},
    activeLightMentorPk: '',
    defaultExtendedMentor: {
      address: "",
      date_of_birth: "",
      email: "",
      first_name: "",
      last_name: "",
      licence_key: "",
      phone_number: "",
      profile_image: "/static/img/empty-img.png",
      questionnaire_creation_date: "",
      responsible: soc_service_id,
      status: "NOT_SPECIFIED"
    },
    mentorSocServiceData: {},
    socServiceId: soc_service_id,
    searchString: ''
  },
  created() {
    this.extendedMentor = Object.assign({}, this.defaultExtendedMentor);
    this.getLightData();
  },
  methods: {
    getLightData() {
      $.get('?get_light_data', (res) => {
        this.lightMentors = res.mentors_data;
        this.searchedMentors = this.lightMentors;
        this.mentorStatuses = res.mentor_statuses;
        this.publicServices = res.public_services;
      })
    },
    getExtendedMentorData(mentorId) {
      this.expanded = !this.expanded;

      if (this.expanded) {
        $.get(`?get_extended_data&mentor_id=${mentorId}`, (res) => {
          this.extendedMentor = res.mentor_data;
          this.mentorSocServiceData = res.mentor_social_service_center_data;
        });
      }
    },
    submitMentorCard() {
      const formData = new FormData();
      for (let key in this.extendedMentor) {
          if (this.extendedMentor.hasOwnProperty(key)) {
              formData.append(key, this.extendedMentor[key]);
          }
      }

      $.ajax({
        url: 'change_extended_data/',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
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
      const formData = new FormData();
      for (let key in this.mentorSocServiceData) {
          if (this.mentorSocServiceData.hasOwnProperty(key)) {
              formData.append(key, this.mentorSocServiceData[key]);
          }
      }

      $.ajax({
        url: 'change_social_service_center_data/',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
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
    },
    addMentorModal() {
      this.expanded = false;
      this.extendedMentor = Object.assign({}, this.defaultExtendedMentor);
      this.extendedMentor.password1 = '';
      this.extendedMentor.password2 = '';
    },
    changeProfileImage(event) {
      this.extendedMentor.profile_image = event.target.files[0];
    },
    deleteProfileImage() {
      this.extendedMentor.profile_image = this.defaultExtendedMentor.profile_image;
    },
    getImageUrl(img) {
      return typeof img === 'string' ? img : URL.createObjectURL(img);
    }
  },
  watch: {
    lightMentors: {
      handler: function (oldVal, newVal) {
        if (newVal.length) {
          const val = newVal.find(v => v.pk === this.activeLightMentorPk);
          const formData = new FormData();
          for (let key in val) {
              if (val.hasOwnProperty(key)) {
                  formData.append(key, val[key]);
              }
          }

          $.ajax({
            url: 'change_light_data/',
            data: formData,
            processData: false,
            contentType: false,
            cache: false,
            enctype: 'multipart/form-data',
            type: 'POST',
          });
        }
      },
      deep: true
    },
    searchString: function (newSearchString) {
      const searchableFields = ['questionnaire__full_name', 'licence_key__key', 'docs_status'];
      this.searchedMentors = this.lightMentors.filter(m => {
        let searched = false;

        for (let field of searchableFields) {
          if (m[field] && !searched) {
            console.log(m[field], newSearchString, m[field].toLowerCase().includes(newSearchString.toLowerCase()));
            searched = m[field].toLowerCase().includes(newSearchString.toLowerCase());
          }
        }

        if (!searched) {
          searched = this.mentorStatuses[m['status']].toLowerCase().includes(newSearchString.toLowerCase());
        }

        for (let service of this.publicServices) {
          if (service.pk === m['responsible']) {
            if (!searched) {
              searched = service.name.toLowerCase().includes(newSearchString.toLowerCase())
            }
          }
        }

        if (!searched) {
          searched = 'ЦССДМ'.toLowerCase().includes(newSearchString.toLowerCase());
        }
        return searched;
      });
    }
  }
});
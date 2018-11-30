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
    phoneView: false,
    mentorModalDisplay: false,
    extendedMentor: {},
    activeLightMentorPk: '',
    defaultExtendedMentor: {
      actual_address: "",
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
    searchString: '',
    docsStatuses: [],
    errors: {}
  },
  created() {
    this.extendedMentor = Object.assign({}, this.defaultExtendedMentor);
    this.getLightData();
  },
  methods: {
    getLightData() {
      $.get('/social-service/mentors/?get_light_data', (res) => {
        this.lightMentors = res.mentors_data;
        this.searchedMentors = this.lightMentors;
        this.docsStatuses = res.docs_statuses;
        this.mentorStatuses = res.mentor_statuses;
        this.publicServices = res.public_services;
      })
    },
    getExtendedMentorData(mentorId) {
      this.expanded = !this.expanded;

      if (this.expanded) {
        $.get(`/social-service/mentors/?get_extended_data&mentor_id=${mentorId}`, (res) => {
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
      const thisContext = this;

      $.ajax({
        url: '/social-service/mentors/change_extended_data/',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
        type: 'POST',
        success: (res) => {
          if (res.pk) {
            if (!this.extendedMentor.pk) {
              const lightMentor = {
                'pk': res.pk,
                'coordinator_id': res.coordinator_id,
                'docs_status': res.docs_status,
                'full_name': `${this.extendedMentor.first_name} ${this.extendedMentor.last_name}`,
                'licence_key__key': this.extendedMentor.licence_key__key,
                'phone_number': this.extendedMentor.phone_number,
                'responsible': this.extendedMentor.responsible,
                'status': this.extendedMentor.status,
                'user_id': res.pk
              }
              thisContext.lightMentors.push(lightMentor);
            }
            this.mentorModalDisplay = false;
            this.mentorCardView = true;
          } else {
            this.errors = res;
          }
        }
      });
    },
    submitMentorSocServeData() {
      const formData = new FormData();
      for (let key in this.mentorSocServiceData) {
          if (this.mentorSocServiceData.hasOwnProperty(key)) {
              if (this.mentorSocServiceData[key]) {
                formData.append(key, this.mentorSocServiceData[key]);
              }
          }
      }

      $.ajax({
        url: '/social-service/mentors/change_social_service_center_data/',
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
      this.mentorModalDisplay = true;
      this.extendedMentor = Object.assign({}, this.defaultExtendedMentor);
      this.extendedMentor.password1 = '';
      this.extendedMentor.password2 = '';
    },
    closeMentorCard() {
      this.mentorModalDisplay = false;
    },
    changeProfileImage(event) {
      this.extendedMentor.profile_image = event.target.files[0];
    },
    deleteProfileImage() {
      this.extendedMentor.profile_image = this.defaultExtendedMentor.profile_image;
    },
    getImageUrl(img) {
      return typeof img === 'string' ? img : URL.createObjectURL(img);
    },
    getResponsibleName(respPK) {
      const pubService = this.publicServices.find(p => p.pk === respPK);
      return pubService ? pubService.name : 'ЦССДМ'
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
            url: '/social-service/mentors/change_light_data/',
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
      const searchableFields = ['full_name', 'licence_key__key', 'docs_status'];
      this.searchedMentors = this.lightMentors.filter(m => {
        let searched = false;

        for (let field of searchableFields) {
          if (m[field] && !searched) {
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
    },
    extendedMentor: {
      handler: function (newObj) {
        const lightObj = this.lightMentors.find(m => m.pk === newObj.pk);

        if (lightObj) {
          const index = this.lightMentors.indexOf(lightObj);

          const newLightMentor = {
            'pk': newObj.pk,
            'full_name': `${newObj.first_name} ${newObj.last_name}`,
            'status': newObj.status,
            'licence_key__key': newObj.licence_key,
            'responsible': newObj.responsible,
            'docs_status': lightObj.docs_status,
            'phone_number': newObj.phone_number,
          }
          this.lightMentors.splice(index, 1);
          this.lightMentors.splice(index, 0, newLightMentor);
        }
      },
      deep: true
    },
    mentorSocServiceData: {
      handler: function (newObj) {
        const activeLightMentor = this.lightMentors.find(m => m.pk === this.activeLightMentorPk);

        if (newObj.certificate_of_good_conduct
          && newObj.medical_certificate && newObj.passport_copy && newObj.application) {
          activeLightMentor.docs_status = 'ALL';
        } else if (newObj.certificate_of_good_conduct
          || newObj.medical_certificate || newObj.passport_copy || newObj.application) {
          activeLightMentor.docs_status = 'NOT_ALL';
        } else {
          activeLightMentor.docs_status = 'NOTHING';
        }

        this.submitMentorSocServeData();
      },
      deep: true
    }
  }
});
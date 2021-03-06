const publicServices = new Vue({
  el: '#public-services',
  delimiters: ['[[', ']]'],
  data: {
    lightPublicServices: [],
    publicServiceStatuses: {},
    defaultExtendedPublicService: {
      name: "",
      max_pair_count: 0,
      phone_number: "",
      email: "",
      address: "",
      website: "",
      contract_number: "",
      profile_image: "/static/img/empty-img.png",
      pair_count: 0,
      status: "NOT_SPECIFIED",
      mentorPk: "",
      organizationPk: ""
    },
    extendedPublicService: {},
    mentorList: [],
    organizationList: [],
    mentorsData: [],
    mentorStatuses: {},
    publicServices: [],
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
    extendedMentor: {},
    errors: {},

    activeLightPublicServicePk: '',

    publicServiceDetail: false,
    mentorModalDisplay: false,
    mentorModalView: true,
    publicServiceView: true,
    publicServiceModalDisplay: false
  },
  created() {
    this.extendedMentor = this.defaultExtendedMentor;
    this.getPublicServiceLightData();
  },
  methods: {
    getPublicServiceLightData() {
      $.get('/social-service/public-services/?get_light_public_service_data', (res) => {
        this.lightPublicServices = res.service_data;
        this.publicServiceStatuses = res.public_service_statuses;
        this.mentorList = res.mentor_list;
        this.organizationList = res.organization_list;
      })
    },
    getExtendedMentorData(mentorId) {
      $.get(`/social-service/mentors/?get_extended_data&mentor_id=${mentorId}`, (res) => {
        this.extendedMentor = res.mentor_data;

        this.mentorModalDisplay = true;
      });
    },
    getExtendedPublicServiceData(publicServicePk) {
      if (!this.publicServiceDetail) {
        $.get(`/social-service/public-services/?get_extended_public_service_data&public_service_pk=${publicServicePk}`, (res) => {
          this.extendedPublicService = res.public_service_data;
          this.extendedPublicService.mentorPk = '';
          this.extendedPublicService.organizationPk = '';
          this.mentorsData = res.mentors_data;
          this.publicServices = res.public_services;
          this.mentorStatuses = res.mentor_statuses;

          this.publicServiceDetail = true;
        })
      } else {
        this.publicServiceDetail = false;
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
        url: '/social-service/mentors/change_extended_data/',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
        type: 'POST',
        success: (res) => {
          if (res.status === 'success') {
            this.mentorModalDisplay = false;
          } else {
            this.errors = res;
          }
        }
      });
    },
    closeMentorCard() {
      this.mentorModalDisplay = false;
      this.extendedMentor = this.defaultExtendedMentor;
    },
    addPublicService() {
      this.extendedPublicService = this.defaultExtendedPublicService;
      this.publicServiceDetail = false;
      this.publicServiceModalDisplay = true;
    },
    changeProfileImage(event) {
      this.extendedMentor.profile_image = event.target.files[0];
    },
    deleteProfileImage() {
      this.extendedMentor.profile_image = this.defaultExtendedMentor.profile_image;
    },
    changePublicServiceProfileImage(event) {
      this.extendedPublicService.profile_image = event.target.files[0];
    },
    deletePublicServiceProfileImage() {
      this.extendedPublicService.profile_image = this.defaultExtendedPublicService.profile_image;
    },
    getImageUrl(img) {
      return typeof img === 'string' ? img : URL.createObjectURL(img);
    },

    submitPublicService() {
      const formData = new FormData();
      for (let key in this.extendedPublicService) {
          if (this.extendedPublicService.hasOwnProperty(key)) {
              if (this.extendedPublicService[key]) {
                formData.append(key, this.extendedPublicService[key]);
              }
          }
      }

      $.ajax({
        url: '/social-service/public-services/change_extended_data/',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
        type: 'POST',
        success: (res) => {
          if (res.status === 'success') {
            this.errors = {};
            this.publicServiceModalDisplay = false;
          } else {
            this.errors = res;
          }
        }
      });
    }
  },
  watch: {
    lightPublicServices: {
      handler: function (oldVal, newVal) {
        if (newVal.length) {
          const val = newVal.find(v => v.pk === this.activeLightPublicServicePk);

          const formData = new FormData();
          for (let key in val) {
              if (val.hasOwnProperty(key)) {
                  formData.append(key, val[key]);
              }
          }

          $.ajax({
            url: '/social-service/public-services/change_light_data/',
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
    }
  }
});
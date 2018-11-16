const publicServices = new Vue({
  el: '#public-services',
  delimiters: ['[[', ']]'],
  data: {
    lightPublicServices: [],
    publicServiceStatuses: {},
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

    publicServiceDetail: false,
    mentorModalDisplay: false,
    mentorModalView: true,
    publicServiceView: true
  },
  created() {
    this.getPublicServiceLightData();
    this.extendedMentor = this.defaultExtendedMentor;
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
        console.log(res.mentor_data);
        this.extendedMentor = res.mentor_data;

        this.mentorModalDisplay = true;
      });
    },
    getExtendedPublicServiceData(publicServicePk) {
      $.get(`/social-service/public-services/?get_extended_public_service_data&public_service_pk=${publicServicePk}`, (res) => {
        this.extendedPublicService = res.public_service_data;
        this.mentorsData = res.mentors_data;
        this.publicServices = res.public_services;
        this.mentorStatuses = res.mentor_statuses;

        this.publicServiceDetail = true;
      })
    },
    submitMentorCard() {},
    closeMentorCard() {
      this.mentorModalDisplay = false;
      this.extendedMentor = this.defaultExtendedMentor;
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

  }
});
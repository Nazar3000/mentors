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

    publicServiceDetail: false,
    mentorModalDisplay: false,
    mentorModalView: true,
    publicServiceView: true
  },
  created() {
    this.getPublicServiceLightData();
  },
  methods: {
    getPublicServiceLightData() {
      $.get('?get_light_public_service_data', (res) => {
        this.lightPublicServices = res.service_data;
        this.publicServiceStatuses = res.public_service_statuses;
        this.mentorList = res.mentor_list;
        this.organizationList = res.organization_list;
      })
    },
    getExtendedPublicServiceData(publicServicePk) {
      $.get(`?get_extended_public_service_data&public_service_pk=${publicServicePk}`, (res) => {
        this.extendedPublicService = res.public_service_data;
        this.mentorsData = res.mentors_data;

        this.publicServiceDetail = true;
      })
    },

  },
  watch: {

  }
});
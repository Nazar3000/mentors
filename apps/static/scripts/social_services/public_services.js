const publicServices = new Vue({
  el: '#public-services',
  delimiters: ['[[', ']]'],
  data: {
    lightPublicServices: [],
    publicServiceStatuses: {},
    extendedPublicService: {}
  },
  created() {
    this.getPublicServiceLightData();
  },
  methods: {
    getPublicServiceLightData() {
      $.get('?get_light_public_service_data', (res) => {
        this.lightPublicServices = res.service_data;
        this.publicServiceStatuses = res.public_service_statuses;
      })
    },
    getExtendedPublicServiceData(publicServicePk) {
      $.get(`?get_extended_public_service_data&public_service_pk=${publicServicePk}`, (res) => {
        this.extendedPublicService = res.public_service_data;
      })
    },

  },
  watch: {

  }
});
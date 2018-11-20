const vm = new Vue({
  el: '#pair-card',
  delimiters: ['[[', ']]'],
  data: {
    pairData: {},
    startDate: '',
    endDate: '',
    publicServices: [
      {
        'pk': '',
        'name': ''
      }
    ],
    mentorStatuses: {},
    organizations: [],
    statuses: {},
    viewMode: true,
    soc_service_id: '',
    errors: {}
  },
  created() {
    $.get('?get_pair_data', (res) => {
      this.soc_service_id = soc_service_id;
      this.pairData = res.pair_data;
      this.startDate = res.interaction_dates.start_date;
      this.endDate = res.interaction_dates.end_date;
      this.publicServices = res.public_services;
      this.mentorStatuses = res.mentor_statuses;
      this.organizations = res.organizations;
      this.statuses = res.statuses;
    });
  },
  methods: {
    submit() {

    },
    findPublicService() {
      const publicService = this.publicServices.find(p => p.pk === this.pairData.responsible)
      if (publicService) {
        return publicService.name
      }
      return ''
    }
  }
});
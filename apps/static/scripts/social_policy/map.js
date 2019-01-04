new Vue({
  el: '#map-ukraine',
  delimiters: ['[[', ']]'],
  data: {
    selectedDistrictId: '',
    districtData: []
  },
  created() {
  },
  methods: {
    showInfo(districtId) {
      console.log(districtId);
    },
    handleStateClick (e) {
      $.get(`?district_id=${this.selectedDistrictId}`, (res) => {
        this.districtData = res;
      })
    },
    handleStateHover (e) {
      if (e.target.tagName === 'path' && e.target.dataset.id) {
        this.selectedDistrictId = e.target.dataset.id;
      }
    }
  },
  watch: {
  }
});
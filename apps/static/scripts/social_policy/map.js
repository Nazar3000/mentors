new Vue({
  el: '#map-ukraine',
  delimiters: ['[[', ']]'],
  data: {
    selectedDistrictId: '',
    districtData: {},

    searchValue: '',
    selectedSocialService: {},
    searchedSocialServices: []
  },
  methods: {
    showInfo(districtId) {
      console.log(districtId);
    },
    handleStateClick() {
      $.get(`?district_id=${this.selectedDistrictId}`, (res) => {
        this.districtData = res;
      })
    },
    handleStateHover(e) {
      if (e.target.tagName === 'path' && e.target.dataset.id) {
        this.selectedDistrictId = e.target.dataset.id;
      }
    },
    selectSocialService(socService) {
      this.selectedSocialService=socService;
      this.searchedSocialServices=[];
      this.searchValue = this.selectedSocialService.name;

      $.get(`?social_service_id=${this.selectedSocialService.pk}`, (res) => {
        this.districtData = res;
      });
    },
    getPercentage(val1, val2) {
      if (val2 !== 0) {
        let divideValue = (val1 / val2).toFixed(3);
        if (divideValue === '0.000') {
          divideValue = '0';
        }
        return divideValue
      }
      return 0
    }
  },
  watch: {
    searchValue: function (newVal) {
      if (newVal && this.selectedSocialService.name !== this.searchValue) {
        $.get(`?search_value=${newVal}&district_id=${this.selectedDistrictId}`, (res) => {
          this.searchedSocialServices = res;
        });
      } else {
        this.searchedSocialServices = [];
        this.handleStateClick();
      }
    }
  }
});
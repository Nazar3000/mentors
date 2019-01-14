new Vue({
  el: '#map-ukraine',
  delimiters: ['[[', ']]'],
  data: {
    selectedDistrictId: '',
    districtData: {},

    searchValue: '',
    selectedSocialService: {},
    searchedSocialServices: [],
    regions: {
      UKR283: 'Сімферополь',
      UKR284: 'Миколаївська',
      UKR285: 'Чернігівський',
      UKR286: 'Рівненська',
      UKR288: 'Чернівецька',
      UKR289: 'Івано-Франківська',
      UKR290: 'Хмельницька',
      UKR291: 'Львівська',
      UKR292: 'Тернопільська',
      UKR293: 'Закарпатська',
      UKR318: 'Волинська',
      UKR319: 'Черкаська',
      UKR320: 'Кіровоградська',
      UKR321: 'Київська',
      UKR322: 'Одеська',
      UKR323: 'Вінницька',
      UKR324: 'Житомирська',
      UKR325: 'Сумська',
      UKR326: 'Дніпропетровська',
      UKR327: 'Донецька',
      UKR328: 'Харківська',
      UKR329: 'Луганська',
      UKR330: 'Полтавська',
      UKR331: 'Запорізька',
      UKR4827: 'Херсонська',
      UKR5482: 'Сімферополь'
    }
  },
  methods: {
    showInfo(districtId) {
      console.log(districtId);
    },
    handleStateClick() {
      $.get(`?district_id=${this.regions[regionId]}`, (res) => {
        this.districtData = res;
      })
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
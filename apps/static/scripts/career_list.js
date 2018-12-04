const careerList = new Vue({
  el: '#career-list',
  delimiters: ['[[', ']]'],
  data: {
    proforientations: [],
    searchedProforientations: [],
    selected_proforientation: {
      related_mentors: []
    },
    agreed: false,
    userId: '',
    new_org: {},
    default_new_org: {
      company_name: '',
      profession_name: '',
      address: '',
      meeting_days: '',
      business_description: '',
      phone_number: ''
    },
    showModal: false,
    errors: [],
    searchString: '',
    map: {},
    defaultCoordinates: {
      lat: 50.4501,
      lng: 30.5234
    }
  },
  created() {
    this.new_org = this.default_new_org;

    $.get('?get_careers', (res) => {
      this.proforientations = res;
      this.searchedProforientations = this.proforientations;
    })


  },
  mounted: function () {
    this.map = new google.maps.Map(document.getElementById('map'), {
      zoom: 15,
      center: this.defaultCoordinates
    });
  },
  methods: {
    selectProforientation(proforientation) {
      this.selected_proforientation = proforientation;
      if (this.selected_proforientation.related_mentors.includes(userId)) {
        this.agreed = true;
      }
      $('.career-modal').fadeIn(500);
    },
    unselectProforientation() {
      this.selected_proforientation = {};
      $('.career-modal').fadeOut(400);
    },
    submitRelation() {
      if (this.agreed && !(this.selected_proforientation.related_mentors.includes(userId))) {
        this.selected_proforientation.related_mentors.push(userId);
        this.proforientations.find(
          p => p.id === this.selected_proforientation.id).related_mentors.push(userId);
      } else if (!this.agreed && this.selected_proforientation.related_mentors.includes(userId)) {
        const relatedId = this.proforientations.find(
          p => p.id === this.selected_proforientation.id).related_mentors.indexOf(userId);
        this.proforientations.find(
          p => p.id === this.selected_proforientation.id).related_mentors.splice(relatedId, 1);
      }
      this.unselectProforientation();
    },
    submitForm() {
      let formData = new FormData();
      for (let key in this.new_org) {
          if (this.new_org.hasOwnProperty(key)) {
              if (this.new_org[key]) {
                formData.append(key, this.new_org[key]);
              }
          }
      }

      $.ajax({
        url: '?add_career',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'x-www-form-urlencoded',
        type: 'POST',
        success: (res) => {
          if (res.pk) {
            this.new_org.id = res.pk;
            this.new_org.related_mentors = res.related_mentors;
            this.proforientations.push(this.new_org);
            this.new_org = this.default_new_org;
            this.showModal = false;
          } else {
            this.errors = res;
          }
        }
      });
    },
    findOnMap(address) {
      let map = this.map;
      let geocoder = new google.maps.Geocoder();
      geocoder.geocode({'address': address}, function (results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
          if (status !== google.maps.GeocoderStatus.ZERO_RESULTS) {
            map.setCenter(results[0].geometry.location);
            let marker = new google.maps.Marker({
              position: results[0].geometry.location,
              map: map
            });
          } else {
            console.log('No results found')
          }
        } else {
          console.log('Geocode was not successful for the following reason: ' + status)
        }
      });
    }
  },
  watch: {
    searchString: function (newSearchString) {
      const searchableFields = ['profession_name', 'company_name', 'address'];
      this.searchedProforientations = this.proforientations.filter(m => {
        let searched = false;

        for (let field of searchableFields) {
          if (m[field] && !searched) {
            searched = m[field].toLowerCase().includes(newSearchString.toLowerCase());
          }
        }
        return searched;
      });
    }
  }
});
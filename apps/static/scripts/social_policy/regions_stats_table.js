new Vue({
  el: '#regions-stats-table',
  delimiters: ['[[', ']]'],
  data: {
    regions_data: [],
    sliceSize: 3,
    currentSortField: ''

  },
  created() {
    $.get('?regions_table', (res) => {
      this.regions_data = res;
    })
  },
  methods: {
    getPercentage(val1, val2) {
      if (val2 !== 0) {
        let divideValue = (val1 / val2).toFixed(3);
        if (divideValue === '0.000') {
          divideValue = '0';
        }
        return divideValue
      }
      return 0
    },
    changeSliceSize() {
      this.sliceSize = this.sliceSize === 3 ? this.regions_data.length : 3;
    },
    dynamicSort(property) {
      let sortOrder = 1;
      if (property[0] === '-') {
        sortOrder = -1;
        property = property.substr(1)
      }
      return function (a, b) {
        let result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
        return result * sortOrder
      }
    },
    reverseSort(field) {
      if (field !== this.currentSortField) {
        this.regions_data = this.regions_data.sort(this.dynamicSort(`-${field}`));

        this.currentSortField = field;
      } else {
        this.regions_data = this.regions_data.sort(this.dynamicSort(field));

        this.currentSortField = '';
      }
    }
  },
});
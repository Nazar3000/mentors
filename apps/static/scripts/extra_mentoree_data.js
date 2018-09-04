const extraMentoreeData = new Vue({
  el: '#extra-data-fields',
  delimiters: ['[[', ']]'],
  data: {
    dataFields: [],

    sliceStart: 0,
    sliceEnd: 0,
    sliceStep: 5,
    pageCount: 0,
    activePageNumber: 1
  },
  created() {
    this.dataFields = JSON.parse(extraDataFields);

    this.sliceEnd += this.sliceStep;
    this.pageCount = Math.ceil(Object.keys(this.dataFields).length / this.sliceStep)
  },
  methods: {
    paginate(pageNumber) {
      this.sliceStart = (pageNumber * this.sliceStep) - this.sliceStep;
      this.sliceEnd = pageNumber * this.sliceStep;
        this.activePageNumber = pageNumber;
    }
  }
});
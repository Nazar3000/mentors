const extraMentoreeData = new Vue({
  el: '#extra-data-fields',
  delimiters: ['[[', ']]'],
  data: {
    dataFields: [],
    emptyDataFieldKeyIndexes: [],
    emptyDataFieldValueIndexes: [],

    sliceStart: 0,
    sliceEnd: 0,
    sliceStep: 5,
    pageCount: 0,
    activePageNumber: 1,

    viewMode: true
  },
  created() {
    this.dataFields = JSON.parse(extraDataFields);
    this.sliceEnd += this.sliceStep;
    this.getPageCount()
  },
  methods: {
    getPageCount() {
      this.pageCount = Math.ceil(Object.keys(this.dataFields).length / this.sliceStep);
    },
    paginate(pageNumber) {
      this.sliceStart = (pageNumber * this.sliceStep) - this.sliceStep;
      this.sliceEnd = pageNumber * this.sliceStep;
        this.activePageNumber = pageNumber;
    },
    addNewExtraDataField() {
      this.dataFields.unshift({});
      this.getPageCount();
    },
    removeDataField(index) {
      this.dataFields.splice(index, 1);
      this.getPageCount();
    },
    saveDataFields() {
      let hasEmptyFields = false;
      for (let i = 0; i < this.dataFields.length; i++) {
        if (!Object.keys(this.dataFields[i]).length || !Object.keys(this.dataFields[i])[0]) {
          this.emptyDataFieldKeyIndexes.push(i);
          hasEmptyFields = true;
        }
        if (!Object.values(this.dataFields[i]).length || !Object.values(this.dataFields[i])[0]) {
          this.emptyDataFieldValueIndexes.push(i);
          hasEmptyFields = true;
        }
      }

      if (!hasEmptyFields) {
        this.viewMode = true;

        $.post('', {'data': JSON.stringify(this.dataFields), 'user_id': userId});
      }
    },
    changeDataFieldThemeData(index, value) {
      const dataValue = Object.values(this.dataFields[index])[0];
      this.dataFields[index] = {
        [value]: dataValue ? dataValue : ''};
    },
    changeDataFieldValueData(index, value) {
      const dataKey = Object.keys(this.dataFields[index])[0];
      this.dataFields[index] = {
        [dataKey ? dataKey : '']: value};
    }
  }
});
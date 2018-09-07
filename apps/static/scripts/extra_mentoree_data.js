$.get('?get_mentoree_data', function (mentoreeData) {

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
    this.dataFields = mentoreeData['extra_data_fields'];
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

        $.post('', {'extra_fields_data': JSON.stringify(this.dataFields), 'user_id': userId});
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

const mentoreeDetailEdit = new Vue({
  el: '#mentoree-detail-edit',
  delimiters: ['[[', ']]'],
  data: {
    mentoreeData: mentoreeData,
    uploadedImageUrl: null,
    viewMode: true
  },
  created() {
    this.uploadedImageUrl = this.mentoreeData.profile_image;
  },
  methods: {
    changeProfileImage(event) {
      this.mentoreeData.profile_image = event.target.files[0];
      this.uploadedImageUrl = URL.createObjectURL(this.mentoreeData.profile_image);
    },
    updateMentoreeData() {

    },
    deleteProfileImage() {
      this.mentoreeData.profile_image = null;
      this.uploadedImageUrl = null;
    },
    submitMentoreeData() {
      let formData = new FormData();
      formData.append('mentoree_data', '');
      formData.append('user_id', userId);
      formData.append('first_name', this.mentoreeData['first_name']);
      formData.append('last_name', this.mentoreeData['last_name']);
      formData.append('date_of_birth', this.mentoreeData['date_of_birth']);
      formData.append('dream', this.mentoreeData['dream']);
      formData.append('want_to_become', this.mentoreeData['want_to_become']);
      formData.append('fears', this.mentoreeData['fears']);
      formData.append('loves', this.mentoreeData['loves']);
      formData.append('hates', this.mentoreeData['hates']);
      formData.append('strengths', this.mentoreeData['strengths']);
      formData.append('extra_data', this.mentoreeData['extra_data']);
      formData.append('profile_image', this.mentoreeData['profile_image']);

      $.ajax({
        url: '',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
        type: 'POST',
        success: () => {
          this.viewMode = true;
        }
      });
    }
  }
});

});
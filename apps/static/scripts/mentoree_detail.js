$.get('?get_mentoree_data', function (mentoreeData) {
  let newMentoree = false;
  if (!mentoreeData.id) {
    mentoreeData = {
      address: "",
      age: "",
      date_of_birth: "",
      dream: "",
      extra_data: "",
      extra_data_fields: [],
      fears: "",
      first_name: "",
      hates: "",
      id:  null,
      last_name: "",
      loves: "",
      organization: "",
      all_organizations: mentoreeData.all_organizations,
      profile_image: "",
      story: "",
      story_images: [],
      strengths: "",
      want_to_become: "",
    };
    newMentoree = true;
  }

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
    this.dataFields = mentoreeData['extra_data_fields']
      ? mentoreeData['extra_data_fields']
      : this.dataFields;
    this.sliceStep = this.dataFields.length >= this.sliceStep
      ? this.sliceStep
      : this.dataFields.length;
    this.sliceEnd += this.sliceStep;
    this.getPageCount();
    if (newMentoree) {
      this.viewMode = false;
    }
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
    organizationObject: null,
    viewMode: true
  },
  created() {
    this.uploadedImageUrl = this.mentoreeData.profile_image;
    this.organizationObject = this.mentoreeData.all_organizations.find(o => {
      return o.id === this.mentoreeData.organization;
    });
    this.mentoreeData.organization = this.mentoreeData.organization
      ? this.mentoreeData.organization
      : this.mentoreeData.all_organizations[0].id;
    if (newMentoree) {
      this.viewMode = false;
    }
  },
  methods: {
    changeProfileImage(event) {
      this.mentoreeData.profile_image = event.target.files[0];
      this.uploadedImageUrl = URL.createObjectURL(this.mentoreeData.profile_image);
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
      formData.append('organization_id', this.mentoreeData['organization']);

      $.ajax({
        url: '',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
        type: 'POST',
        success: () => {
          this.organizationObject = this.mentoreeData.all_organizations.find(o => {
            return o.id === this.mentoreeData.organization;
          });
          this.viewMode = true;
        }
      });
    }
  }
});

const mentoreeStory = new Vue({
  el: '#mentoree-story',
  delimiters: ['[[', ']]'],
  data: {
    story: mentoreeData.story,
    images: mentoreeData.story_images,
    currentImage: '/static/img/user.svg',
    viewMode: true
  },
  created() {
    if (this.images.length) {
      this.currentImage = this.images[0];
    }
    if (newMentoree) {
      this.viewMode = false;
    }
  },
  methods: {
    prevImage() {
      const currImgIndex = this.images.indexOf(this.currentImage);
      if (currImgIndex > 0) {
        this.currentImage = this.images[currImgIndex - 1];
      }
      else {
        this.currentImage = this.images[this.images.length - 1];
      }
    },
    nextImage() {
      const currImgIndex = this.images.indexOf(this.currentImage);
      if (currImgIndex < this.images.length - 1) {
        this.currentImage = this.images[currImgIndex + 1];
      }
      else {
        this.currentImage = this.images[0];
      }
    },
    deleteImage() {
      const currImgIndex = this.images.indexOf(this.currentImage);
      this.images.splice(currImgIndex, 1);
      if (!this.images.length) {
        this.currentImage = '/static/img/user.svg';
      }
      else {
        this.prevImage();
      }
    },
    getFileObjectUrl(fileObject) {
      return URL.createObjectURL(fileObject)
    },
    addImage(event) {
      this.images.push(event.target.files[0]);
      this.currentImage = this.images[this.images.length - 1];
    },
    submitStoryData() {
      let formData = new FormData();
      formData.append('mentoree_story', '');
      formData.append('user_id', userId);
      formData.append('story', this.story);

      const oldImages = this.images.filter(i => typeof i === 'string');
      formData.append('old_images', oldImages);
      const newImages = this.images.filter(i => i instanceof File);
      newImages.map((img, index) => {
        if (img instanceof File) {
          formData.append(`new_image_${index}`, img);
        }
      });
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
$.get('/mentor/mentoree/?get_mentoree_data', function (mentoreeData) {
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
        formData.append('profile_image', this.mentoreeData['profile_image']);
        formData.append('organization_id', this.mentoreeData['organization']);

        $.ajax({
          url: '/mentor/mentoree/',
          data: formData,
          processData: false,
          contentType: false,
          cache: false,
          enctype: 'multipart/form-data',
          type: 'POST',
          success: (res) => {
            console.log(res);
            this.viewMode = false;
            // this.organizationObject = this.mentoreeData.all_organizations.find(o => {
            //   return o.id === this.mentoreeData.organization;
            // });
            // this.viewMode = true;
          }
        });
      }
    }
  });

});
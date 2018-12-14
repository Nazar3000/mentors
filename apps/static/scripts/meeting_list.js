const meetingList = new Vue({
  el: '#meeting-list',
  delimiters: ['[[', ']]'],
  data: {
    meetings: [],
    errors: {},
    modes: {
      collapsed: 0,
      expanded: 1,
      edit: 2
    },
    itemAdding: false,
    imgAdded: false
  },
  created() {
    $.get('?get_meetings_data', (data) => {
      if (data.length) {
        this.meetings = data.map(m => {
          m.mode = this.modes.collapsed;
          return m;
        });
      }
      this.imgAdded = true;
    });
    if (window.location.search.substring(1).includes('newMeeting')) {
      this.insertNewMeeting();
    }
  },
  methods: {
    deleteMeeting(meetingId) {
      if (meetingId) {
        $.post('', {'meeting_id': meetingId, 'delete_meeting': true}, (data) => {
          if (data.status === 'success') {
            const index = this.meetings.indexOf(this.meetings.find(m => m.id === meetingId));
            this.meetings.splice(index, 1);
          }
        })
      } else {
        const index = this.meetings.indexOf(this.meetings.find(m => m.id === meetingId));
        this.meetings.splice(index, 1);
        this.itemAdding = false;
      }
    },
    addImage(event, meetingId) {
      const images = this.meetings.find(m => m.id === meetingId).images;
      images.push(event.target.files[0]);

      const formData = new FormData();
      formData.append('image', event.target.files[0]);
      formData.append('image_data', '');
      formData.append('meeting_id', meetingId);
      $.ajax({
        url: '',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
        type: 'POST'
      });
    },
    getImageUrl(img) {
      return typeof img === 'string' ? img : URL.createObjectURL(img);
    },
    addNewMeetingImage(event, meeting) {
      if (!meeting.id) {
        meeting.images.push(event.target.files[0]);
      } else {
        this.addImage(event, meeting.id)
      }
      this.imgAdded = true;
    },
    changeMeeting(meeting) {
      const formData = new FormData();
      formData.append('new_meeting', '');
      meeting.images.map((img, index) => {
        if (img instanceof File) {
          formData.append(`new_image_${index}`, img);
        }
      });

      const newMeeting = Object.assign({}, meeting);
      delete newMeeting['images'];
      for (let key in newMeeting) {
          if (newMeeting.hasOwnProperty(key)) {
              formData.append(key, newMeeting[key]);
          }
      }
      $.ajax({
        url: '',
        data: formData,
        processData: false,
        contentType: false,
        cache: false,
        enctype: 'multipart/form-data',
        type: 'POST',
        success: (res) => {
          if (res.errors) {
            delete res.errors;
            this.errors = res;
          } else {
            this.errors = {};
            meeting = this.meetings.find(m => m.id === meeting.id);
            if (meeting) {
              meeting.mode = this.modes.collapsed;
            } else {
              this.meetings.push(res);
            }
            this.itemAdding = false;
          }
        }
      });
    },
    editMeeting(meetingId) {
      this.meetings.find(m => m.id === meetingId).mode = this.modes.edit;
    },
    insertNewMeeting() {
      this.meetings.unshift({
        date: '',
        description: '',
        images: [],
        note_for_next_meeting: '',
        observation: '',
        title: '',
        mode: this.modes.edit
      });
      this.itemAdding = true;
    },
  },
  watch: {
    imgAdded: function (value) {
      if (value) {
        setTimeout(function() {
          console.log($('.lSSlideOuter').length)
          if ($('.lSSlideOuter').length) {
            $('.lSSlideOuter').lightSlider().destroy()
            // slider.destroy();
          }
          $('.vertical').lightSlider({
              gallery: true,
              item: 1,
              vertical: true,
              verticalHeight: 250,
              vThumbWidth: 70,
              thumbItem: 4,
              thumbMargin: 0,
              slideMargin: 0,
          });
        }, 300);
      }
      this.imgAdded = false;
    }
  }
});

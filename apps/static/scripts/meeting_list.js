const meetingList = new Vue({
  el: '#meeting-list',
  delimiters: ['[[', ']]'],
  data: {
    meetings: [],
    collapsedView: true
  },
  created() {
    $.get('?get_meetings_data', (data) => {
      this.meetings = data;
    });
  },
  methods: {
    deleteMeeting(meetingId) {
      $.post('', {'meeting_id': meetingId, 'delete_meeting': true}, (data) => {
        if (data.status === 'success') {
          const index = this.meetings.indexOf(this.meetings.find(m => m.id === meetingId));
          this.meetings.splice(index, 1);
        }
      })
    },
    addImage(event, meetingId) {
      const images = this.meetings.find(m => m.id === meetingId).images;
      images.push(event.target.files[0]);

      console.log('here');
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
    }
  }
});
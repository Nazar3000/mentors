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
    }
  }
});
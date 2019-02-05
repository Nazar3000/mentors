// const notifications = new Vue({
//   el: '#notifications',
//   delimiters: ['[[', ']]'],
//   data: {
//     modes: {
//       empty: 0,
//       nonEmptySwallowed: 1,
//       nonEmptyExpanded: 2,
//     },
//     currentMode: 0,
//     notifications: []
//   },
//   created() {
//     this.getNotifications();
//   },
//   methods: {
//     getNotifications() {
//       $.get('/mentor/notifications/', (res) => {
//         this.notifications = res;
//         if (this.notifications.length > 0) {
//           this.currentMode = this.modes.nonEmptySwallowed;
//         }
//       })
//     },
//     changeMode() {
//       if (this.currentMode === this.modes.nonEmptySwallowed) {
//         this.currentMode = this.modes.nonEmptyExpanded;
//       } else if (this.currentMode === this.modes.nonEmptyExpanded) {
//         this.currentMode = this.modes.nonEmptySwallowed;
//       }
//     },
//     markAsRead(notificationId) {
//       console.log(notificationId);
//       $.post('/mentor/notifications/', {'notification_id': notificationId}, (res) => {
//         console.log('here');
//       })
//     }
//   }
// });
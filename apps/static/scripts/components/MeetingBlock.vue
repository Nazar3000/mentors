<template>
  <div class="diary-wrapp" id="meeting-block">
    <div class="diary-header">
      <div class="diary-header-link"><a href=""><i class="fas fa-plus"></i></a><span>Додати зустріч</span></div>
    </div>
    <template v-for="meeting in meetingsData" v-if="!expanded">
      <MeetingCollapsed :meeting="meeting" @clicked="changeIsCollapsed"></MeetingCollapsed>
    </template>
    <template v-for="meeting in meetingsData" v-else>
      <MeetingExtended :meeting="meeting" @clicked="changeIsCollapsed"></MeetingExtended>
    </template>
  </div>
</template>

<script>
  import jQuery from 'jquery';
  import MeetingCollapsed from './MeetingCollapsed.vue';
  import MeetingExtended from './MeetingExtended.vue';

  export default {
    name: 'MeetingBlock',
    components: {
      MeetingCollapsed,
      MeetingExtended
    },
    data() {
      return {
        meetingsData: [],
        expanded: false
      }
    },
    created() {
      jQuery.get('?get_meetings_data', (meetingsData) => {
        this.meetingsData = meetingsData;
      });
    },
    methods: {
      changeIsCollapsed(value) {
        this.expanded = value;
      }
    }
  }
</script>

<style scoped>

</style>
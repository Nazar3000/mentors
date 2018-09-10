<template>
  <div class="diary-block" data-id="1">
      <div class="diary-card">
        <h2>{{ meeting.title }}</h2>
        <div class="diary-line"></div><span>{{ meeting.date }}</span>
        <p>{{ meeting.description }}</p>
        <a class="block-open-more"
           href="javascript: void(0)"
           @click="$emit('clicked', true)"
        >
          Читати далі
        </a>
      </div>
      <div class="diary-slider">
        <div class="slider-wrap">
          <ul id="vertical">
            <template v-for="img in meeting.images">
              <li :data-thumb="img"><img class="w-100" :src="img"></li>
            </template>
          </ul>
        </div>
      </div>
    </div>
</template>

<script>
  export default {
    name: 'MeetingCollapsed',
    props: ['meeting'],
    created() {
      console.log(this.meeting);
    }
  }
</script>

<style scoped>

</style>
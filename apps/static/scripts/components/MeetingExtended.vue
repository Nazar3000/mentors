<template>
  <div class="diary-block-open" data-id="1" style="display: block">
    <div class="diary-block-wrapp">
      <div class="diary-block-left">
        <h2>{{ meeting.title }}</h2>
        <div class="diary-block-line"></div><span>{{ meeting.date }}</span>
      </div>
      <div class="diary-block-right">
        <div class="diary-block-link">
          <div class="diary-block-link-item"><a class="diary-block-frown" href=""><i class="far fa-frown"></i></a><span>Фото дня не завантажені</span></div>
          <div class="diary-block-link-item"><a class="diary-block-img" href=""><i class="fas fa-plus"></i></a><span>Додати фото</span></div>
          <div class="diary-block-link-item"><a class="diary-block-edit" href=""><i class="fas fa-pencil-alt"></i></a></div>
        </div>
        <div class="diary-block-trash"><a href=""><i class="fas fa-trash"></i></a></div>
      </div>
    </div>
    <div class="diary-block-content">
      <h4>Опис:</h4>
      <p>{{ meeting.description }}</p>
      <h4>Спостереження за вихованцем:</h4>
      <p>{{ meeting.observation }}</p>
      <h4>Замітка для наступної зустрічі:</h4>
      <p>{{ meeting.note_for_next_meeting }}</p>
      <a class="diary-block-close"
         href="javascript: void(0)"
         @click="$emit('clicked', false)"
      >
        Згорнути
      </a>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'MeetingExtended',
    props: ['meeting']
  }
</script>

<style scoped>

</style>
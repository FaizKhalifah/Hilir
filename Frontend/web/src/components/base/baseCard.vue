<template>
  <div class="card" :class="cardClass">
    <header v-if="title" class="card-header">{{ title }}</header>
    <div class="card-content">
      <slot /> <!-- Tempat konten dinamis -->
    </div>
  </div>
</template>

<script>
export default {
  name: "BaseCard",
  props: {
    title: {
      type: String,
      default: ""
    },
    cardClass: {
      type: String,
      default: ""
    }
  }
};
</script>

<style scoped>
.card {
  border: 1px solid #e0e0e0;
  padding: 16px;
  border-radius: 8px;
  background-color: #fff;
}
.card-header {
  font-weight: bold;
  font-size: 24px;
}
</style>

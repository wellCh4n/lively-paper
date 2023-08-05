<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  }
})

</script>

<template>
  <div class="area-header">
    {{ props.title }}
  </div>
</template>

<style scoped>
.area-header {
  text-align: center;
  background-color: var(--el-color-primary-dark-2);
  color: var(--el-color-white);
  padding: 5px 0;
  margin: 0 5px;
  border-radius: var(--el-border-radius-base);
}
</style>
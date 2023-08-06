<script setup>
defineProps({
  content: {
    type: String,
    required: false
  }
})
</script>

<template>
  <div style="display: flex; justify-content: right">
    <div class="question-block">
      <p style="word-break: break-all; padding: 0 1rem">{{ content }}</p>
    </div>
    <div style="margin-left: 10px">
      <el-avatar>You</el-avatar>
    </div>
  </div>
</template>

<style scoped>
.question-block {
  text-align: right;
  background-color: #fff;
  border: solid 1px var(--el-border-color);
  border-radius: var(--el-border-radius-base);
  transition: background-color var(--el-transition-duration),color var(--el-transition-duration);
}
.question-block:hover {
  background-color: var(--el-color-primary-light-9);
  color: var(--el-menu-active-color);
  transition: background-color var(--el-transition-duration),color var(--el-transition-duration);
}
</style>
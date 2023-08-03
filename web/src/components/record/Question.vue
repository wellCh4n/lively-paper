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
    <div style="text-align: right; background-color: #f8f8f8">
      <p style="word-break: break-all; padding: 0 1rem">{{ content }}</p>
    </div>
    <div style="margin-left: 10px">
      <el-avatar>You</el-avatar>
    </div>
  </div>
</template>

<style scoped>

</style>
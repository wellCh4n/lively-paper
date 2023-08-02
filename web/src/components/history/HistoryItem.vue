<script setup>
defineProps({
  title: {
    type: String,
    required: true
  }
})
</script>

<template>
  <el-button size="large" style="width: 300px; margin-left: 0">{{ title }}</el-button>
</template>

<style scoped>

</style>
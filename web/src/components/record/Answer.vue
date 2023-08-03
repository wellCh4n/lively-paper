<script setup>
import { onMounted, toRef, reactive } from 'vue'
import VueMarkdown from 'markdown-vue'

const props = defineProps({
  content: {
    type: String,
    required: false
  },
  contentCallback: {
    type: Function
  }
})

const contentParam = reactive({
  content: props.content
})

onMounted(() => {
  if (props.contentCallback === undefined) {
    contentParam.content = props.content
  } else {
    props.contentCallback(contentParam.content, (str) => {
      contentParam.content = str
    })
  }
})
</script>

<template>
  <div style="display: flex;">
    <div style="margin-right: 1em">
      <el-avatar>Paper</el-avatar>
    </div>
    <div style="background-color: #f8f8f8; padding: 0 1rem;">
      <VueMarkdown :source="contentParam.content"/>
<!--      <p style="word-break: break-all; padding: 0 1rem;">{{ contentParam.content }}</p>-->
    </div>
  </div>
</template>

<style scoped>

</style>
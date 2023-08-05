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
    <div class="answer-block">
      <VueMarkdown :source="contentParam.content"/>
<!--      <p style="word-break: break-all; padding: 0 1rem;">{{ contentParam.content }}</p>-->
    </div>
  </div>
</template>

<style scoped>
.answer-block {
  background-color: #fff;
  padding: 0 1rem;
  border: solid 1px var(--el-border-color);
  border-radius: var(--el-border-radius-base);
}
</style>
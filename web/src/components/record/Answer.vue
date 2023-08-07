<script setup>
import { onMounted, reactive, ref } from 'vue'
import VueMarkdown from 'markdown-vue'
import { DocumentCopy } from '@element-plus/icons-vue'

const copyMessage = 'Copy Answer'
const copiedMessage = 'Copied!'
const copyTooltipContent = ref(copyMessage)

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

const copyAnswer = () => {
  const type = "text/plain";
  const blob = new Blob([contentParam.content], { type })
  const data = [new ClipboardItem({ [type]: blob })]
  navigator.clipboard.write(data).then(() => {
    copyTooltipContent.value = copiedMessage
    setTimeout(() => {
      copyTooltipContent.value = copyMessage
    }, 1000)
  })
}

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
    </div>
    <el-tooltip
        effect="dark"
        :content="copyTooltipContent"
        placement="top-end"
    >
      <el-button :icon="DocumentCopy"
                 plain @click="copyAnswer"
                 size="small"
                 style="margin-left: 5px"
      />
    </el-tooltip>
  </div>
</template>

<style scoped>
.answer-block {
  background-color: #fff;
  padding: 0 1rem;
  border: solid 1px var(--el-border-color);
  border-radius: var(--el-border-radius-base);
  transition: background-color var(--el-transition-duration),color var(--el-transition-duration);
}
.answer-block:hover {
  color: var(--el-menu-active-color);
  background-color: var(--el-color-primary-light-9);
  transition: background-color var(--el-transition-duration),color var(--el-transition-duration);
}
</style>
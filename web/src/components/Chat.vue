<script setup>
import { reactive, onMounted, ref, watch, defineExpose } from 'vue'
import { Position } from '@element-plus/icons-vue'
import Record from '@/components/record/Record.vue'

const emit = defineEmits(['new-chat', 'add-chat'])

const recordsView = ref()
const form = reactive({
  prompt: ''
})
const records = ref([])
const currentRecord = ref('')

const submit = () => {
  if (form.prompt === '') {
    return
  }
  const prompt = form.prompt
  if (records.value.length === 0) {
    emit('new-chat', prompt)
    emit('add-chat', currentRecord.value)
  }
  records.value.push({
    question: prompt,
    answer: '',
    answerCallback: async (answer, setAnswer) => {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          query: prompt,
          mode: 'streaming',
          id: currentRecord.value.id
        })
      })
      const reader = response.body.getReader()
      while(true) {
        const { done, value } = await reader.read()
        if (done) {
          break
        }
        const word = new TextDecoder().decode(value)
        answer += word
        setAnswer(answer)
      }
    }
  })
  form.prompt = ''
}

const recordsViewToBottom = () => {
  const height = recordsView.value.wrapRef.scrollHeight
  recordsView.value.setScrollTop(height)
}

onMounted(() => {
  recordsViewToBottom()
})

watch(() => form.prompt, (current, _) => {
  if (current && current.startsWith('/') && current.length === 1) {
    console.log('触发魔法')
  }
})

watch(() => records.value.length, () => {
  recordsViewToBottom()
})

const onHistorySwitch = (item) => {
  currentRecord.value = item
  records.value = []
}

defineExpose({
  onHistorySwitch
})

</script>

<template>
  <div style="display: flex; flex-direction: column-reverse; width: 100%; position: relative; margin: 0 1rem">
    <el-scrollbar style="width: 100%; margin-top: 1rem; margin-bottom: 100px" ref="recordsView">
      <Record v-for="item in records"
              :key="item.question"
              :question="item.question"
              :answer="item.answer"
              :answerCallback="item.answerCallback"
      />
    </el-scrollbar>
    <div style="width: 100%; justify-content: center; text-align: center; height: 60px; line-height: 60px; border-bottom: 1px solid var(--el-border-color);">
      {{ currentRecord.title ? currentRecord.title : '跃然纸上' }}
    </div>

    <el-form @submit.native.prevent
             @submit="submit"
             :model="form"
             style="width: 100%; position: absolute; bottom: 20px; boxShadow: var(--el-box-shadow)"
    >
      <el-form-item style="margin-bottom: 0;">
        <el-input autofocus
                  v-model="form.prompt"
                  style="height: 50px;">
          <template #append>
            <el-button :icon="Position" />
          </template>
        </el-input>
      </el-form-item>
    </el-form>
  </div>

</template>

<style scoped>
</style>
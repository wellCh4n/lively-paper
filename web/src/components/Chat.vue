<script setup>
import { reactive, onMounted, ref, watch, defineExpose } from 'vue'
import { Position } from '@element-plus/icons-vue'
import Record from '@/components/record/Record.vue'
import { get } from '@/utils/request'
import AreaHeader from "@/components/AreaHeader.vue";

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
  return true
})

const onHistorySwitch = (item, isNew) => {
  if (item.id === currentRecord.value.id) {
    return
  }
  currentRecord.value = item
  if (isNew) {
    records.value = []
  }
  if (!isNew) {
    get(`/chat/history/${item.id}`).then((res) => {
      records.value = res
    })
  }
}

defineExpose({
  onHistorySwitch
})

</script>

<template>
  <div class="chat-wrapper">
    <AreaHeader :title="currentRecord.title ? currentRecord.title : 'Lively Paper'" style="margin-top: 5px"/>
    <el-scrollbar style="width: 100%;  margin-bottom: 90px; border-bottom: solid 1px var(--el-border-color);"
                  ref="recordsView">
      <Record v-for="item in records"
              :key="item.question"
              :question="item.question"
              :answer="item.answer"
              :answerCallback="item.answerCallback"
              class="record"
      />
    </el-scrollbar>

    <el-form @submit.native.prevent
             @submit="submit"
             :model="form"
             style="width: 100%; position: absolute; bottom: 20px;"
    >
      <el-form-item style="margin-bottom: 0; background-color: var(--el-color-info-light-9)">
        <el-input autofocus
                  v-model="form.prompt"
                  style="height: 50px; box-shadow: var(--el-box-shadow); margin: 0 2rem">
          <template #append>
            <el-button :icon="Position" />
          </template>
        </el-input>
      </el-form-item>
    </el-form>
  </div>

</template>

<style scoped>
.chat-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  position: relative;
  margin-left: 5px;
  background-color: var(--el-color-info-light-9);
  border-radius: var(--el-border-radius-base);
}
.record:last-of-type {
  padding-bottom: 1rem;
}
</style>
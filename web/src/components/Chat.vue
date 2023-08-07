<script setup>
import { reactive, ref, watch, defineExpose, nextTick, getCurrentInstance } from 'vue'
import { Position } from '@element-plus/icons-vue'
import Record from '@/components/record/Record.vue'
import { get } from '@/utils/request'
import AreaHeader from "@/components/AreaHeader.vue"
import {matchMagic} from "@/components/magic/magic"

const emit = defineEmits(['new-chat', 'add-chat'])

const recordsRef = ref()
const form = reactive({
  prompt: ''
})
const records = ref([])
const recordRef = ref()
const currentRecord = ref('')
const promptInput = ref()
const inputDisable = ref(false)
const instance = getCurrentInstance()
const activatedMagic = ref()

const submit = () => {
  if (form.prompt === '' || inputDisable.value) {
    return
  }
  if (activatedMagic.value) {
    activatedMagic.value.fn(instance)
    activatedMagic.value = null
    form.prompt = ''
    return;
  }
  inputDisable.value = true
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
        body: JSON.stringify({ query: prompt, mode: 'streaming', id: currentRecord.value.id })
      })
      const reader = response.body.getReader()
      while (true) {
        const { done, value } = await reader.read()
        if (done) {
          inputDisable.value = false
          break
        }
        const word = new TextDecoder().decode(value)
        answer += word
        setAnswer(answer)
        recordsViewToBottom()
      }
    }
  })
  form.prompt = ''
}

const recordsViewToBottom = () => {
  nextTick(() => {
    const height = recordRef.value.clientHeight
    recordsRef.value.setScrollTop(height)
  })
}

watch(() => form.prompt, (current, _) => {
  if (current && current.startsWith('/')) {
    const magic = matchMagic(current)
    if (magic) activatedMagic.value = {fn: magic.fn}
  }
  return true
})

const onHistorySwitch = (item, isNew) => {
  if (item.id === currentRecord.value.id) {
    return
  }
  currentRecord.value = item
  if (isNew) {
    document.title = 'Lively Paper - 跃然纸上'
    records.value = []
  }
  if (!isNew) {
    document.title = `${item.title} - Lively Paper - 跃然纸上`
    records.value = []
    get(`/chat/history/${item.id}`).then((res) => {
      records.value = res
      recordsViewToBottom()
    })
  }
  promptInput.value.focus()
}

defineExpose({
  onHistorySwitch
})

</script>

<template>
  <div class="chat-wrapper">
    <AreaHeader :title="currentRecord.title ? currentRecord.title : 'Lively Paper'" style="margin-top: 5px"/>
    <el-scrollbar style="width: 100%;  margin-bottom: 90px; border-bottom: solid 1px var(--el-border-color);"
                  ref="recordsRef">
      <div ref="recordRef">
        <Record v-for="item in records"
              :key="item._id"
              :question="item.question"
              :answer="item.answer"
              :answerCallback="item.answerCallback"
              class="record"
        />
      </div>
    </el-scrollbar>

    <el-form @submit.native.prevent
             @submit="submit"
             :model="form"
             style="width: 100%; position: absolute; bottom: 20px;"
    >
      <el-form-item style="margin-bottom: 0; background-color: var(--el-color-info-light-9)">
        <el-input autofocus
                  v-model="form.prompt"
                  placeholder="Send a message"
                  style="height: 50px; box-shadow: var(--el-box-shadow); margin: 0 2rem"
                  ref="promptInput"
        >
          <template #append>
            <el-button :icon="Position"
                       @click="submit"
                       :disabled="inputDisable"
                       class="submit-btn"
            />
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
.submit-btn {
  background-color: var(--el-color-primary) !important;
  height: 50px;
  color: #fff !important;
}
.submit-btn:hover {
  background-color: var(--el-color-primary-light-3) !important;
}
</style>